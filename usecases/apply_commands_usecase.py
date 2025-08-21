from time import sleep

import structlog

from dataproviders.daichicloud.command_registry import ClimateCommandsEnum
from dataproviders.daichicloud.daichicloud_api import DaichiCloudClient
from dataproviders.homeassistant_mqtt.dto import MQTTDeviceTopicControlEnum
from dataproviders.homeassistant_mqtt.mqtt_provider import HomeAssistantMQTTClimateProvider

# TODO: Нужен кеш последнено полкучения стетейта
#  или дисковери или применения команды, тогда будет понятно нужно ли делать лишний запрос на получение состояния
log = structlog.get_logger()


class ApplyCommandsUseCase:
    """
        Apply commands from homeassistant
    """

    def __init__(self, daichi: DaichiCloudClient, mqtt_provider: HomeAssistantMQTTClimateProvider,
                 enable_silence_mode=True):
        self.daichi = daichi
        self.mqtt_provider = mqtt_provider
        self.enable_silence_mode = enable_silence_mode

    def execute(self, device_id: int, topic_type: MQTTDeviceTopicControlEnum, payload: str | int):
        # TODO: Если устройства нет в памяти реестра, то и стейтов нет, а значит нефиг сейчас исполнять
        # Mode ["off", "cool", "heat", "auto", "fan_only", "dry"]
        _for_apply = list()
        if topic_type == MQTTDeviceTopicControlEnum.MODE_SET:
            mode_to_commands = {
                'off': [
                    {'command': ClimateCommandsEnum.POWER, 'payload': False}
                ],
                'cool': [
                    {'command': ClimateCommandsEnum.POWER, 'payload': True},
                    {'command': ClimateCommandsEnum.SET_CLIMATE_MODE_COOL, 'payload': True}
                ],
                'heat': [
                    {'command': ClimateCommandsEnum.POWER, 'payload': True},
                    {'command': ClimateCommandsEnum.SET_CLIMATE_MODE_HEAT, 'payload': True}
                ],
                'auto': [
                    {'command': ClimateCommandsEnum.POWER, 'payload': True},
                    {'command': ClimateCommandsEnum.SET_CLIMATE_MODE_AUTO, 'payload': True}
                ],
                'fan_only': [
                    {'command': ClimateCommandsEnum.POWER, 'payload': True},
                    {'command': ClimateCommandsEnum.SET_CLIMATE_MODE_FAN, 'payload': True}
                ],
                'dry': [
                    {'command': ClimateCommandsEnum.POWER, 'payload': True},
                    {'command': ClimateCommandsEnum.SET_CLIMATE_MODE_DRY, 'payload': True}
                ],
            }
            if payload in mode_to_commands.keys():
                _for_apply += mode_to_commands[payload]

        if topic_type == MQTTDeviceTopicControlEnum.TEMPERATURE_SET:
            _for_apply += [
                {'command': ClimateCommandsEnum.SET_TEMP, 'payload': int(payload)},
            ]

        if topic_type == MQTTDeviceTopicControlEnum.FAN_SET:
            # Fan speed ["auto", "low", "medium", "high"]
            fan_speed_to_commands = {
                'auto': [
                    {'command': ClimateCommandsEnum.SET_FAN_SPEED_AUTO, 'payload': True},
                ],
                'low': [
                    {'command': ClimateCommandsEnum.SET_FAN_SPEED, 'payload': 1},
                ],
                'medium': [
                    {'command': ClimateCommandsEnum.SET_FAN_SPEED, 'payload': 2},
                ],
                'high': [
                    {'command': ClimateCommandsEnum.SET_FAN_SPEED, 'payload': 3},
                ],
            }
            if payload in fan_speed_to_commands.keys():
                _for_apply += fan_speed_to_commands[payload]

        if len(_for_apply) == 0:
            log.error(f'Unsupport payload={payload} or topic_type={topic_type}')

        if len(_for_apply) > 0:
            if self.enable_silence_mode:
                _mute_sound = [{'command': ClimateCommandsEnum.FUNC_MUTE_SOUND, 'payload': True}, ]
                _for_apply = _mute_sound + _for_apply

        for apply_item in _for_apply:
            log.info(f"Execute commands {apply_item['command']} for device_id={device_id}")
            self.daichi.execute_command(device_id=device_id, command=apply_item['command'],
                                        payload=apply_item['payload'])

            log.debug(f'Wait 1 seconds between commands')
            sleep(1)
