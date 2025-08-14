import structlog

from dataproviders.homeassistant_mqtt.mqtt_helper import HomeAssistantMQTTHelper

log = structlog.get_logger()


class HomeAssistantMQTTEntrypoint:
    def __init__(self):
        log.info('Init MQTT entrypoint')

    def device_commands_entrypoint(self, mqtt_client, userdata, message):

        if HomeAssistantMQTTHelper.has_support_topic(message.topic):
            topic_type = HomeAssistantMQTTHelper.classify_topic(message.topic)
            daichi_cloud_device_id = HomeAssistantMQTTHelper.extract_device_id(message.topic)
            log.info(f'Received message: topic={message.topic} '
                     f'topic_type={topic_type} daichi_cloud_device_id={daichi_cloud_device_id} '
                     f'payload={message.payload.decode()}')
        else:
            log.debug("Unsupport topic={message.topic}")
