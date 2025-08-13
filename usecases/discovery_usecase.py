import structlog

from dataproviders.daichicloud.command_registry import ClimateCommandsEnum
from dataproviders.daichicloud.daichicloud_api import DaichiCloudClient
from dataproviders.homeassistant_mqtt.dto import MQTTDeviceClimateDescribe, MQTTDeviceClimateDeviceDescribe
from dataproviders.homeassistant_mqtt.mqtt_provider import HomeAssistantMQTTProvider

log = structlog.get_logger()


class DiscoveryClimateDeviceUseCase:
    """
        Looking for device and publish to homeassistant
    """

    def __init__(self, daichi: DaichiCloudClient, mqtt_provider: HomeAssistantMQTTProvider):
        self.daichi = daichi
        self.mqtt_provider = mqtt_provider

    def execute(self):
        buildings = self.daichi.get_buildings()
        # TODO: Берем только первое строение, явно нужно переделать
        first_building = buildings.pop()
        for place in first_building.places:
            self.mqtt_provider.publish_discovery(device=self._make_describe_of_device(place=place))
            # self._publish_to_mqtt_describe(place=place)
            # self._publish_to_states(place=place)
            # self._publish_to_sensor(place=place)

    def _make_describe_of_device(self, place) -> MQTTDeviceClimateDescribe:
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
        return device

    def _publish_to_mqtt_describe(self, place):
        pass

    def _publish_to_sensor(self, place):
        pass

    def _publish_to_states(self, place):
        pass
