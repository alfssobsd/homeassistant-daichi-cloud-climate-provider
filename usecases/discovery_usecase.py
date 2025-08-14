import structlog

from dataproviders.daichicloud.command_registry import ClimateCommandsEnum
from dataproviders.daichicloud.daichicloud_api import DaichiCloudClient
from dataproviders.daichicloud.dto import Place
from dataproviders.homeassistant_mqtt.dto import MQTTDeviceClimateDescribe, MQTTDeviceClimateDeviceDescribe
from dataproviders.homeassistant_mqtt.mqtt_provider import HomeAssistantMQTTClimateProvider

log = structlog.get_logger()


class DiscoveryClimateDeviceUseCase:
    """
        Looking for device and publish to homeassistant
    """

    def __init__(self, daichi: DaichiCloudClient, mqtt_provider: HomeAssistantMQTTClimateProvider):
        self.daichi = daichi
        self.mqtt_provider = mqtt_provider

    def execute(self):
        buildings = self.daichi.get_buildings()
        # TODO: Берем только первое строение, явно нужно переделать
        first_building = buildings.pop()
        for place in first_building.places:
            device = self._make_describe_of_device(place=place)
            self.mqtt_provider.publish_discovery(device=device)
            self._restore_states(device=device, place=place)
            # self._publish_to_states(place=place)
            # self._publish_to_sensor(place=place)

    def _make_describe_of_device(self, place: Place) -> MQTTDeviceClimateDescribe:
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

    def _restore_states(self, device: MQTTDeviceClimateDescribe, place: Place):
        # TODO: Доделать реализацию
        if place.sensor_temp is not None:
            self.mqtt_provider.publish_state(state_topic=device.temperature_state_topic(), payload=place.sensor_temp)

        if place.state.is_on:
            self.mqtt_provider.publish_state(state_topic=device.power_command_topic(), payload="ON")
        else:
            self.mqtt_provider.publish_state(state_topic=device.power_command_topic(), payload="OFF")

        # if place.sensor_temp is not None:
        #     self.mqtt_provider.publish_state(state_topic=device.temperature_state_topic(), payload=place.sensor_temp)

