from dataproviders.daichicloud.command_registry import ClimateCommandsEnum
from dataproviders.daichicloud.dto import Place, ClimateStatePayloadTypeEnum
from dataproviders.homeassistant_mqtt.dto import MQTTDeviceClimateDescribe
from dataproviders.homeassistant_mqtt.mqtt_provider import HomeAssistantMQTTClimateProvider


# TODO: Что есть все преобразовать в команды и восстанавливать используя команды переданные сюда? А где-то будет преобразователь?
class RestoreStateClimateDeviceUseCase:
    def __init__(self, mqtt_provider: HomeAssistantMQTTClimateProvider):
        self.mqtt_provider = mqtt_provider

    def execute(self, device: MQTTDeviceClimateDescribe, place: Place):
        if place.sensor_temp is not None:
            self.mqtt_provider.publish_state(state_topic=device.current_temperature_topic, payload=place.sensor_temp)

        if place.state is not None and place.state.is_on == False:  # False -> OFF
            self.mqtt_provider.publish_state(state_topic=device.mode_state_topic, payload='off')

        if place.state is not None and place.state.details is not None:
            for detail_item in place.state.details:
                detail_payload = detail_item.payload

                # Mode ["off", "cool", "heat", "auto", "fan_only", "dry"]
                if detail_payload.climate_state_type == ClimateStatePayloadTypeEnum.CLIMATE_MODE:
                    if place.state.is_on:
                        if detail_payload.command == ClimateCommandsEnum.SET_CLIMATE_MODE_COOL:
                            self.mqtt_provider.publish_state(state_topic=device.mode_state_topic, payload='cool')
                        if detail_payload.command == ClimateCommandsEnum.SET_CLIMATE_MODE_HEAT:
                            self.mqtt_provider.publish_state(state_topic=device.mode_state_topic, payload='heat')
                        if detail_payload.command == ClimateCommandsEnum.SET_CLIMATE_MODE_AUTO:
                            self.mqtt_provider.publish_state(state_topic=device.mode_state_topic, payload='auto')
                        if detail_payload.command == ClimateCommandsEnum.SET_CLIMATE_MODE_DRY:
                            self.mqtt_provider.publish_state(state_topic=device.mode_state_topic, payload='dry')
                        if detail_payload.command == ClimateCommandsEnum.SET_CLIMATE_MODE_FAN:
                            self.mqtt_provider.publish_state(state_topic=device.mode_state_topic, payload='fan_only')

                # Fan speed ["auto", "low", "medium", "high"]
                if detail_payload.climate_state_type == ClimateStatePayloadTypeEnum.FAN_SPEED:
                    speed_to_text = {
                        1: 'low',
                        2: 'medium',
                        3: 'high'
                    }
                    if detail_payload.command == ClimateCommandsEnum.SET_FAN_SPEED:
                        self.mqtt_provider.publish_state(state_topic=device.fan_mode_state_topic,
                                                         payload=speed_to_text[detail_payload.value])
                    if detail_payload.command == ClimateCommandsEnum.SET_FAN_SPEED_AUTO:
                        self.mqtt_provider.publish_state(state_topic=device.fan_mode_state_topic,
                                                         payload='auto')

                # Current set temperature C
                if detail_payload.climate_state_type == ClimateStatePayloadTypeEnum.SET_TEMP_C:
                    if detail_payload.command == ClimateCommandsEnum.SET_TEMP:
                        self.mqtt_provider.publish_state(state_topic=device.temperature_state_topic,
                                                         payload=detail_payload.value)

                # Current set temperature F
                if detail_payload.climate_state_type == ClimateStatePayloadTypeEnum.SET_TEMP_F:
                    if detail_payload.command == ClimateCommandsEnum.SET_TEMP:
                        self.mqtt_provider.publish_state(state_topic=device.temperature_state_topic,
                                                         payload=detail_payload.value)
