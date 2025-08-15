import enum
from typing import Optional

from pydantic import BaseModel, computed_field

from dataproviders.homeassistant_mqtt import MQTT_QUEUE_HOMEASSISTANT_NODE_ID_PREFIX, \
    MQTT_QUEUE_HOMEASSISTANT_DEVICE_ID_PREFIX, MQTT_QUEUE_PROVIDER_TOPIC_CLIMATE_DEVICE


class MQTTDeviceTopicControlEnum(str, enum.Enum):
    MODE_SET = 'ac/mode/set'
    MODE_STATE = 'ac/mode/state'
    FAN_SET = 'ac/fan/set'
    FAN_STATE = 'ac/fan/state'
    TEMPERATURE_SET = 'ac/temperature/set'
    TEMPERATURE_STATE = 'ac/temperature/state'
    TEMPERATURE_CURRENT = 'ac/temperature_curr/state'
    UNKNOWN = 'unknown'


class MQTTDeviceClimateDeviceDescribe(BaseModel):
    serial_number: Optional[str]

    @computed_field()
    def model(self) -> str:
        return 'Daichi Cloud Climatizador'


class MQTTDeviceClimateDescribe(BaseModel):
    original_dachi_cloud_id: int
    name: str
    min_temp: int
    max_temp: int
    device: MQTTDeviceClimateDeviceDescribe

    @computed_field
    def unique_id(self) -> str:
        return f'{MQTT_QUEUE_HOMEASSISTANT_NODE_ID_PREFIX}{self.original_dachi_cloud_id}'

    @computed_field
    def payload_on(self) -> str:
        return 'ON'

    @computed_field
    def payload_off(self) -> str:
        return 'OFF'

    #### modes
    @computed_field
    def modes(self) -> list:
        return ["off", "cool", "heat", "auto", "fan_only", "dry"]

    @computed_field
    def mode_command_topic(self) -> str:
        return f'{MQTT_QUEUE_PROVIDER_TOPIC_CLIMATE_DEVICE}/{self._node_id_device_id()}/{MQTTDeviceTopicControlEnum.MODE_SET.value}'

    @computed_field
    def mode_state_topic(self) -> str:
        return f'{MQTT_QUEUE_PROVIDER_TOPIC_CLIMATE_DEVICE}/{self._node_id_device_id()}/{MQTTDeviceTopicControlEnum.MODE_STATE.value}'

    #### fans
    @computed_field
    def fan_modes(self) -> list:
        return ["auto", "low", "medium", "high"]

    @computed_field
    def fan_mode_command_topic(self) -> str:
        return f'{MQTT_QUEUE_PROVIDER_TOPIC_CLIMATE_DEVICE}/{self._node_id_device_id()}/{MQTTDeviceTopicControlEnum.FAN_SET.value}'

    @computed_field
    def fan_mode_state_topic(self) -> str:
        return f'{MQTT_QUEUE_PROVIDER_TOPIC_CLIMATE_DEVICE}/{self._node_id_device_id()}/{MQTTDeviceTopicControlEnum.FAN_STATE.value}'

    #### temperature
    @computed_field
    def temperature_command_topic(self) -> str:
        return f'{MQTT_QUEUE_PROVIDER_TOPIC_CLIMATE_DEVICE}/{self._node_id_device_id()}/{MQTTDeviceTopicControlEnum.TEMPERATURE_SET.value}'

    @computed_field
    def temperature_state_topic(self) -> str:
        return f'{MQTT_QUEUE_PROVIDER_TOPIC_CLIMATE_DEVICE}/{self._node_id_device_id()}/{MQTTDeviceTopicControlEnum.TEMPERATURE_STATE.value}'

    @computed_field
    def current_temperature_topic(self) -> str:
        return f'{MQTT_QUEUE_PROVIDER_TOPIC_CLIMATE_DEVICE}/{self._node_id_device_id()}/{MQTTDeviceTopicControlEnum.TEMPERATURE_CURRENT.value}'

    def _node_id_device_id(self):
        return f'{MQTT_QUEUE_HOMEASSISTANT_DEVICE_ID_PREFIX}{self.original_dachi_cloud_id}'

    #### generate topic for homeassistant
    def discovery_device_climate_topic(self) -> str:
        return f'homeassistant/climate/{self.unique_id}/climate/config'
