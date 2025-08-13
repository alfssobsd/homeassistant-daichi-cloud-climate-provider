import structlog

log = structlog.get_logger()


class HomeAssistantMQTTEntrypoint:
    def __init__(self):
        pass

    def device_commands_entrypoint(self, mqtt_client, userdata, message):
        log.info(f'Received message: topic={message.topic} payload={message.payload.decode()}')
