import logging
import os.path
import signal
import sys
import threading
import traceback
from time import sleep

import schedule
import structlog
from dependency_injector.wiring import Provide, inject
from dotenv import load_dotenv
from pydantic.v1 import ValidationError

from conf.di_container_setup import Container
from dataproviders.homeassistant_mqtt.mqtt_helper import HomeAssistantMQTTHelper
from dataproviders.homeassistant_mqtt.mqtt_provider import HomeAssistantMQTTClimateProvider
from entrypoints.cron.cron_entrypoint import CronEntrypoint
from entrypoints.mqtt.mqtt_entrypoint import HomeAssistantMQTTEntrypoint

logging.basicConfig(
    level=logging.DEBUG,
)

structlog.configure(
    processors=[
        structlog.processors.CallsiteParameterAdder(
            [structlog.processors.CallsiteParameter.FILENAME, structlog.processors.CallsiteParameter.LINENO]
        ),
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        structlog.dev.ConsoleRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

log = structlog.get_logger()

def discovery_cron_job(interval=5):
    current_pid = os.getpid()
    schedule_thread_event = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            try:
                while not schedule_thread_event.is_set():
                    schedule.run_pending()
                    sleep(interval)
            except Exception as e_thread:
                log.error(f'Stop running in discovery_cront_job, error: {e_thread}, {type(e_thread).__name__}')
                traceback.print_exc()
                os.kill(current_pid, signal.SIGTERM)

    schedule_thread = ScheduleThread()
    schedule_thread.start()
    log.info("Background task starting...")
    return schedule_thread_event


@inject
def main(
        mqtt_provider: HomeAssistantMQTTClimateProvider = Provide[Container.mqtt_provider],
        mqtt_entrypoint: HomeAssistantMQTTEntrypoint = Provide[Container.mqtt_entrypoint],
        cron_entrypoint: CronEntrypoint = Provide[Container.cron_entrypoint],
) -> None:
    # Start MQTT
    mqtt_provider.set_entrypoint(entrypoint_func=mqtt_entrypoint.device_commands_entrypoint)
    mqtt_provider.set_topics_for_subscribe(topic_mask=HomeAssistantMQTTHelper.get_mask_for_subscribe())
    mqtt_provider.loop_start()
    ## Start Cron
    cron_entrypoint.start_cron()

    cron_thread_event = discovery_cron_job(interval=5)
    main_thread_event = threading.Event()

    def shutdown_by_signal(sig, _):
        log.info(f'Shutdown application by signal (wait 10s) {sig} ({signal.Signals(sig).name})')
        sleep(10)
        main_thread_event.set()  # Unblock .wait and stop
        cron_thread_event.set()

    signal.signal(signal.SIGINT, shutdown_by_signal)
    signal.signal(signal.SIGTERM, shutdown_by_signal)
    main_thread_event.wait()

    # Shutdown process
    mqtt_provider.shutdown()


if __name__ == "__main__":
    log.info("Application is running...")
    if os.path.exists('.env'):
        log.info("Loading .env file ...")
        load_dotenv()

    try:
        container = Container()

        try:
            config_obj = container.config(**os.environ)
        except ValidationError as e:
            log.error(f'Error environment vars: {e}')
            exit(1)

        container.wire(modules=[__name__])
        main(*sys.argv[1:])
    except Exception as e:
        log.error(f'Stop running in main thread (wait 10s), error: {e}, {type(e).__name__}')
        traceback.print_exc()
        sleep(10)

