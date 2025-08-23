import structlog

from dataproviders.daichicloud.command_registry import ClimateCommandsEnum
from dataproviders.daichicloud.daichicloud_api import DaichiCloudClient
from dataproviders.daichicloud.dto import Place, ClimateStatePayloadTypeEnum
from dataproviders.device_repository.device_repo import ClimateDeviceRepository
from dataproviders.device_repository.dto import ClimateDeviceEntity
from dataproviders.homeassistant_mqtt.dto import MQTTDeviceClimateDescribe, MQTTDeviceClimateDeviceDescribe
from dataproviders.homeassistant_mqtt.mqtt_provider import HomeAssistantMQTTClimateProvider
from usecases.restore_state_usecase import RestoreStateClimateDeviceUseCase

log = structlog.get_logger()


class DiscoveryClimateDeviceUseCase:
    def __init__(self, daichi: DaichiCloudClient,
                 climate_device_repo: ClimateDeviceRepository,
                 restore_state_uc: RestoreStateClimateDeviceUseCase,
                 mqtt_provider: HomeAssistantMQTTClimateProvider):
        self.daichi = daichi
        self.climate_device_repo = climate_device_repo
        self.mqtt_provider = mqtt_provider
        self.restore_state_uc = restore_state_uc

    def execute(self):
        """
            Search device in daichi cloud,
            publish discovery to homeassistant and restore state of devices
        :return: None
        """
        buildings = self.daichi.get_buildings()
        for building in buildings:
            for place in building.places:
                device = self._make_describe_of_device(place=place)
                self.mqtt_provider.publish_discovery(device=device)

                _climate_device_entity = self._make_climate_device_entity(mqtt_device_describe=device, place=place)
                self.climate_device_repo.set_device(climate_device=_climate_device_entity)
                self.restore_state_uc.execute(climate_device_id=_climate_device_entity.climate_device_id)

    def _make_describe_of_device(self, place: Place) -> MQTTDeviceClimateDescribe:
        """
            Make and return MQTTDeviceClimateDescribe for publish to mqtt homeassistant
        :param place:
        :return: MQTTDeviceClimateDescribe
        """
        min_temp = ClimateCommandsEnum.SET_TEMP.value.available_value[0]
        max_temp = ClimateCommandsEnum.SET_TEMP.value.available_value[1]
        device = MQTTDeviceClimateDescribe(
            original_dachi_cloud_id=place.id,
            name=place.title,
            min_temp=min_temp,
            max_temp=max_temp,
            device=MQTTDeviceClimateDeviceDescribe(
                serial_number=place.serial,
                name=f'Air Conditioner',
            )
        )
        return device

    def _make_climate_device_entity(self,
                                    mqtt_device_describe: MQTTDeviceClimateDescribe,
                                    place: Place) -> ClimateDeviceEntity:
        """
            Make and return ClimateDeviceEntity for state device
        :param mqtt_device_describe:
        :param place:
        :return: ClimateDeviceEntity
        """

        _command_to_state = {
            # Mode [ "cool", "heat", "auto", "fan_only", "dry"]
            ClimateStatePayloadTypeEnum.CLIMATE_MODE: {
                ClimateCommandsEnum.SET_CLIMATE_MODE_COOL: 'cool',
                ClimateCommandsEnum.SET_CLIMATE_MODE_HEAT: 'heat',
                ClimateCommandsEnum.SET_CLIMATE_MODE_AUTO: 'auto',
                ClimateCommandsEnum.SET_CLIMATE_MODE_DRY: 'dry',
                ClimateCommandsEnum.SET_CLIMATE_MODE_FAN: 'fan_only',
            },

            # Fan speed ["auto", "low", "medium", "high"]
            ClimateStatePayloadTypeEnum.FAN_SPEED: {
                ClimateCommandsEnum.SET_FAN_SPEED: {
                    1: 'low',
                    2: 'medium',
                    3: 'high',
                },
                ClimateCommandsEnum.SET_FAN_SPEED_AUTO: 'auto'
            },
        }

        _climate_device_entity = ClimateDeviceEntity(
            climate_device_id=mqtt_device_describe.original_dachi_cloud_id,
            mode_state_topic=mqtt_device_describe.mode_state_topic,
            fan_mode_state_topic=mqtt_device_describe.fan_mode_state_topic,
            temperature_state_topic=mqtt_device_describe.temperature_state_topic,
            current_temperature_topic=mqtt_device_describe.current_temperature_topic,
            enable_mute_sound=True
        )

        if place.sensor_temp is not None:
            _climate_device_entity.current_temperature_state = place.sensor_temp

        # Set mode -> off
        if place.state is not None and place.state.is_on == False:
            _climate_device_entity.mode_state = 'off'

        if place.state is not None and place.state.details is not None:
            for detail_item in place.state.details:
                detail_payload = detail_item.payload

                # Set mode
                if detail_payload.climate_state_type == ClimateStatePayloadTypeEnum.CLIMATE_MODE:
                    if place.state.is_on:
                        _climate_device_entity.mode_state = _command_to_state[detail_payload.climate_state_type] \
                            [detail_payload.command]

                # Set fan mode
                if (detail_payload.climate_state_type == ClimateStatePayloadTypeEnum.FAN_SPEED
                        and detail_payload.command == ClimateCommandsEnum.SET_FAN_SPEED):
                    _climate_device_entity.fan_mode_state = _command_to_state[detail_payload.climate_state_type] \
                        [detail_payload.command][detail_payload.value]

                if (detail_payload.climate_state_type == ClimateStatePayloadTypeEnum.FAN_SPEED
                        and detail_payload.command == ClimateCommandsEnum.SET_FAN_SPEED_AUTO):
                    _climate_device_entity.fan_mode_state = _command_to_state[detail_payload.climate_state_type] \
                        [detail_payload.command]

                # Current set temperature C
                if detail_payload.climate_state_type == ClimateStatePayloadTypeEnum.SET_TEMP_C:
                    if detail_payload.command == ClimateCommandsEnum.SET_TEMP:
                        _climate_device_entity.temperature_state = detail_payload.value

                # Current set temperature F
                if detail_payload.climate_state_type == ClimateStatePayloadTypeEnum.SET_TEMP_F:
                    if detail_payload.command == ClimateCommandsEnum.SET_TEMP:
                        _climate_device_entity.temperature_state = detail_payload.value

        return _climate_device_entity
