import logging
import os.path

import structlog
from dotenv import load_dotenv

from dataproviders.homeassistant_mqtt.mqtt_helper import HomeAssistantMQTTHelper
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
    if os.path.exists('.env'):
        load_dotenv()

    # daichi = DaichiCloudClient(
    #     username=os.getenv('DAICHI_USER'),
    #     password=os.getenv('DAICHI_PASS')
    # )
    # dc_uc = DiscoveryClimateDeviceUseCase(daichi=daichi)
    # dc_uc.execute()

    log.debug(HomeAssistantMQTTHelper.classify_topic('dachi_cloud_climate/device_id_287350/ac/temperature/set'))
    log.debug(HomeAssistantMQTTHelper.extract_device_id('dachi_cloud_climate/device_id_287350/ac/temperature/set'))
    log.debug(HomeAssistantMQTTHelper.classify_topic('dachi_cloud_climate/device_id_287350/ac/mode/state'))
    log.debug(HomeAssistantMQTTHelper.extract_device_id('dachi_cloud_climate/device_287350/ac/mode/state'))
    log.debug(HomeAssistantMQTTHelper.classify_topic('bbb/device_id_287350/ac/mode/state'))
    log.debug(HomeAssistantMQTTHelper.extract_device_id('bbb/device_id_287350sdsd/ac/mode/state'))
    log.debug(HomeAssistantMQTTHelper.classify_topic('bbb/device_id_287350/ac/mode/33'))

if __name__ == "__main__":
    main()