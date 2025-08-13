import logging
import os.path
import signal
import threading
from time import sleep

import structlog
from dotenv import load_dotenv

from dataproviders.daichicloud.daichicloud_api import DaichiCloudClient
from dataproviders.homeassistant_mqtt.mqtt_helper import HomeAssistantMQTTHelper
from dataproviders.homeassistant_mqtt.mqtt_provider import HomeAssistantMQTTProvider
from entrypoints.mqtt.mqtt_entrypoint import HomeAssistantMQTTEntrypoint
from usecases.discovery_usecase import DiscoveryClimateDeviceUseCase

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

def main():
    log.info("Application is running...")
    if os.path.exists('.env'):
        load_dotenv()

    daichi = DaichiCloudClient(
        username=os.getenv('DAICHI_USER'),
        password=os.getenv('DAICHI_PASS')
    )


    mqtt_entrypoint = HomeAssistantMQTTEntrypoint()
    mqtt_provider = HomeAssistantMQTTProvider(
        host=os.getenv('MQTT_HOST'),
        port=int(os.getenv('MQTT_PORT')),
        username=os.getenv('MQTT_USER'),
        password=os.getenv('MQTT_PASS'),
    )
    mqtt_provider.set_entrypoint(entrypoint_func=mqtt_entrypoint.device_commands_entrypoint)
    mqtt_provider.set_topics_for_subscribe(topic_mask=HomeAssistantMQTTHelper.get_mask_for_subscribe())
    mqtt_provider.loop_start()

    dc_uc = DiscoveryClimateDeviceUseCase(daichi=daichi, mqtt_provider=mqtt_provider)
    dc_uc.execute()

    # log.debug(HomeAssistantMQTTHelper.classify_topic('dachi_cloud_climate/device_id_287350/ac/temperature/set'))
    # log.debug(HomeAssistantMQTTHelper.extract_device_id('dachi_cloud_climate/device_id_287350/ac/temperature/set'))
    # log.debug(HomeAssistantMQTTHelper.classify_topic('dachi_cloud_climate/device_id_287350/ac/mode/state'))
    # log.debug(HomeAssistantMQTTHelper.extract_device_id('dachi_cloud_climate/device_287350/ac/mode/state'))
    # log.debug(HomeAssistantMQTTHelper.classify_topic('bbb/device_id_287350/ac/mode/state'))
    # log.debug(HomeAssistantMQTTHelper.extract_device_id('bbb/device_id_287350sdsd/ac/mode/state'))
    # log.debug(HomeAssistantMQTTHelper.classify_topic('bbb/device_id_287350/ac/mode/33'))

    thread_event = threading.Event()
    def shutdown_by_signal(sig, frame):
        log.info("Shutdown application by signal ctrl+c or SIGTERM")
        thread_event.set() # Unblock .wait and stop

    signal.signal(signal.SIGINT, shutdown_by_signal)
    signal.signal(signal.SIGTERM, shutdown_by_signal)
    thread_event.wait()

    #Shutdown process
    mqtt_provider.shutdown()


if __name__ == "__main__":
    main()