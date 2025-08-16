from dataproviders.device_repository.device_repo import ClimateDeviceRepository
from dataproviders.homeassistant_mqtt.mqtt_provider import HomeAssistantMQTTClimateProvider


class RestoreStateClimateDeviceUseCase:
    def __init__(self,
                 climate_device_repo: ClimateDeviceRepository,
                 mqtt_provider: HomeAssistantMQTTClimateProvider):
        self.climate_device_repo = climate_device_repo
        self.mqtt_provider = mqtt_provider

    def execute(self, climate_device_id: int):
        climate_device_entity = self.climate_device_repo.get_by_id(climate_device_id=climate_device_id)
        if climate_device_entity is not None:
            if climate_device_entity.current_temperature_state is not None:
                self.mqtt_provider.publish_state(state_topic=climate_device_entity.current_temperature_topic,
                                                 payload=climate_device_entity.current_temperature_state)

            if climate_device_entity.mode_state is not None:
                self.mqtt_provider.publish_state(state_topic=climate_device_entity.mode_state_topic,
                                                 payload=climate_device_entity.mode_state)

            if climate_device_entity.fan_mode_state is not None:
                self.mqtt_provider.publish_state(state_topic=climate_device_entity.fan_mode_state_topic,
                                                 payload=climate_device_entity.fan_mode_state)

            if climate_device_entity.temperature_state is not None:
                self.mqtt_provider.publish_state(state_topic=climate_device_entity.temperature_state_topic,
                                                 payload=climate_device_entity.temperature_state)
