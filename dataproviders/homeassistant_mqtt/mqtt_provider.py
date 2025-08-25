import threading

import structlog
from typing_extensions import Literal

from paho.mqtt import client

from dataproviders.homeassistant_mqtt.dto import MQTTDeviceClimateDescribe

log = structlog.get_logger()


class HomeAssistantMQTTClimateProvider:
    def __init__(self, host: str = 'localhost', port: int = 1883,
                 username: str = 'nobody', password='nopass',
                 transport: Literal["tcp", "websockets", "unix"] = 'tcp'):
        self._lock = threading.Lock()
        log.debug(f'Init MQTT Client username={username}, host={host}, port={port}, transport={transport}')
        self.client_mqtt = client.Client(client_id='HomeAssistantMQTTProvider', transport=transport)
        self.client_mqtt.username_pw_set(username=username, password=password)
        self.host = host
        self.port = port

    def start_listen(self, entrypoint_func, topic_mask: str):
        log.info('Starting up MQTT Client')
        def on_connect(client: client.Client, _, __, rc):
            if rc == 0:
                log.info("Connected to MQTT broker")
                client.subscribe(topic=topic_mask, qos=2)
                log.info(f"MQTT subscribe to {topic_mask}")
            else:
                log.error(f"Connection failed with code {rc}")

        self.client_mqtt.on_connect = on_connect
        self.client_mqtt.on_message = entrypoint_func
        self.client_mqtt.connect(host=self.host, port=self.port, keepalive=60)
        self.client_mqtt.loop_start()

    def shutdown(self):
        log.info('Shutdown MQTT Client')
        self.client_mqtt.loop_stop()
        self.client_mqtt.disconnect()

    def publish_state(self, state_topic: str, payload: int | str):
        log.debug(f'Publish state = {payload} to topic = {state_topic}')
        with self._lock:
            self.client_mqtt.publish(
                topic=state_topic,
                payload=payload,
                retain=True
            )

    def publish_discovery(self, device: MQTTDeviceClimateDescribe):
        log.debug(f'Publish device to topic={device.discovery_device_climate_topic()}, device={device.model_dump()}')
        with self._lock:
            self.client_mqtt.publish(
                topic=device.discovery_device_climate_topic(),
                payload=device.model_dump_json(),
                retain=True
            )
