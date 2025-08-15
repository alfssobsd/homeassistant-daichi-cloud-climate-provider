from dataproviders.daichicloud.command_registry import ClimateCommandsEnum
from dataproviders.daichicloud.daichicloud_api import DaichiCloudClient
from dataproviders.homeassistant_mqtt.dto import MQTTDeviceTopicControlEnum


# TODO: Нужен кеш последнено полкучения стетейта
#  или дисковери или применения команды, тогда будет понятно нужно ли делать лишний запрос на получение состояния

class ApplyCommandsUseCase:
    """
        Apply commands from homeassistant
    """

    def __init__(self, daichi: DaichiCloudClient):
        self.daichi = daichi

    def execute(self, device_id: int, topic_type: MQTTDeviceTopicControlEnum, payload: str | int):
        # Mode ["off", "cool", "heat", "auto", "fan_only", "dry"]
        commands = list()
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
            commands = mode_to_commands[payload]

        for command in commands:
            print(command)