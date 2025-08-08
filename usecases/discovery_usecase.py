import structlog

from dataproviders.daichicloud.command_registry import ClimateCommandsEnum
from dataproviders.daichicloud.daichicloud_api import DaichiCloudClient
from dataproviders.homeassistant_mqtt.dto import MQTTDeviceClimateDescribe, MQTTDeviceClimateDeviceDescribe

log = structlog.get_logger()


class DiscoveryClimateDeviceUseCase:
    """
        Looking for device and publish to homeassistant
    """

    def __init__(self, daichi: DaichiCloudClient):
        self.daichi = daichi

    def execute(self):
        buildings = self.daichi.get_buildings()
        first_building = buildings.pop()
        for place in first_building.places:
            self._make_describe_of_device(place=place)
            self._publish_to_mqtt_describe(place=place)
            self._publish_to_states(place=place)
            self._publish_to_sensor(place=place)

    def _make_describe_of_device(self, place):
        min_temp = ClimateCommandsEnum.SET_TEMP.value.available_value[0]
        max_temp = ClimateCommandsEnum.SET_TEMP.value.available_value[1]
        device = MQTTDeviceClimateDescribe(
            original_dachi_cloud_id=place.id,
            name=place.title,
            min_temp=min_temp,
            max_temp=max_temp,
            device=MQTTDeviceClimateDeviceDescribe(
                serial_number=place.serial,
            )
        )
        log.info(device.model_dump())
        log.info(device.discovery_device_climate_topic())

    def _publish_to_mqtt_describe(self, place):
        pass

    def _publish_to_sensor(self, place):
        pass

    def _publish_to_states(self, place):
        pass
