import structlog
from paho.mqtt.client import MQTTMessage, Client

from dataproviders.homeassistant_mqtt.mqtt_helper import HomeAssistantMQTTHelper
from usecases.apply_commands_usecase import ApplyCommandsUseCase

log = structlog.get_logger()


class HomeAssistantMQTTEntrypoint:
    def __init__(self, apply_commands_uc: ApplyCommandsUseCase):
        self.apply_commands_uc = apply_commands_uc

    def device_commands_entrypoint(self, mqtt_client: Client, userdata, message: MQTTMessage):
        # !!! message in topic `command` must not be `retained`
        if HomeAssistantMQTTHelper.has_support_topic(message.topic):
            topic_type = HomeAssistantMQTTHelper.classify_topic(message.topic)
            daichi_cloud_device_id = HomeAssistantMQTTHelper.extract_device_id(message.topic)
            log.debug(f'Received message: topic={message.topic} '
                      f'topic_type={topic_type} daichi_cloud_device_id={daichi_cloud_device_id} '
                      f'payload={message.payload.decode()}')
            self.apply_commands_uc.execute(device_id=int(daichi_cloud_device_id),
                                           topic_type=topic_type,
                                           payload=message.payload.decode())
        else:
            log.debug("Unsupport topic={message.topic}")
