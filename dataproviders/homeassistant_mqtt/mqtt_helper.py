import structlog
import re

from dataproviders.homeassistant_mqtt import MQTT_QUEUE_PROVIDER_TOPIC_CLIMATE_DEVICE
from dataproviders.homeassistant_mqtt.dto import MQTTDeviceTopicControlEnum

_LOG = structlog.get_logger()


class HomeAssistantMQTTHelper:
    @staticmethod
    def classify_topic(topic: str) -> MQTTDeviceTopicControlEnum:
        for topic_control in MQTTDeviceTopicControlEnum:
            if topic.endswith(topic_control.value):
                return topic_control

        return MQTTDeviceTopicControlEnum.UNKNOWN

    @staticmethod
    def extract_device_id(topic: str) -> str | None:
        match = re.search(r"device_id_([^/]+)", topic)
        return match.group(1) if match else None

    @staticmethod
    def has_support_topic(topic) -> bool:
        if topic.startswith(MQTT_QUEUE_PROVIDER_TOPIC_CLIMATE_DEVICE):
            return True
        return False

    @staticmethod
    def get_mask_for_subscribe() -> str:
        return f'{MQTT_QUEUE_PROVIDER_TOPIC_CLIMATE_DEVICE}/+/+/+/+'
