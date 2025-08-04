from enum import Enum
from pprint import pprint

from pydantic import BaseModel, Field, field_validator, computed_field
from typing import Optional, List, Union, Any

from pydantic.v1 import root_validator, validator

from dataproviders.daichicloud.command_registry import ClimateCommandsEnum


class MqttCredentials(BaseModel):
    username: Optional[str]
    password: Optional[str]


class UserData(BaseModel):
    id: int
    mqtt_credentials: Optional[MqttCredentials] = Field(None, alias="mqttUser")


class ControlValueRequest(BaseModel):
    function_id: int = Field(None, alias="functionId")
    value: Optional[int] = Field(None, alias="value")
    is_on: Optional[bool] = Field(None, alias="isOn")
    parameters: Optional[Any] = Field(None, alias="parameters")

class ControlRequest(BaseModel):
    cmdId: int = Field(None, alias="cmdId")
    value: ControlValueRequest = Field(None, alias="value")
    conflictResolveData: None


class PlaceStatusEnum(str, Enum):
    CONNECTED = 'connected'
    DISCONNECTED = "disconnected"

    @classmethod
    def _missing_(cls, value):
        return cls.DISCONNECTED


class AccessEnum(str, Enum):
    OWNER = "owner"
    UNKNOWN = "unknown"

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class ClimateStatePayloadTypeEnum(str, Enum):
    CLIMATE_MODE = 'climate_mode'
    FAN_SPEED = 'fan_speed'
    SET_TEMP_C = 'set_temp_c'
    SET_TEMP_F = 'set_temp_f'
    OPTION_FUNCTION = 'option_function'
    FUNC_HORIZONT_SWING_ON = 'horizont_swing_on'
    FUNC_VERTICAL_SWING_ON = 'vertical_swing_on'
    FUNC_TURBO_ON = 'turbo_on'
    FUNC_ECO_ON = 'eco_on'

class ClimateStatePayload(BaseModel):
    climate_state_type: ClimateStatePayloadTypeEnum
    command: ClimateCommandsEnum | None
    value: bool | int | str

class PlaceDetailItem(BaseModel):
    """
        conditioner current details state and value
    """
    icon_name: Optional[str] = Field(None, alias="iconName")
    text: Optional[str] = Field(None, alias="text")

    @computed_field
    def payload(self) -> ClimateStatePayload | None:
        match self.icon_name:
            # Climate mode
            case 'modeHeat_active':
                return ClimateStatePayload(
                    climate_state_type=ClimateStatePayloadTypeEnum.CLIMATE_MODE,
                    command=ClimateCommandsEnum.SET_CLIMATE_MODE_HEAT,
                    value=True
                )
            case 'modeCool_active':
                return ClimateStatePayload(
                    climate_state_type=ClimateStatePayloadTypeEnum.CLIMATE_MODE,
                    command=ClimateCommandsEnum.SET_CLIMATE_MODE_COOL,
                    value=True
                )
            case 'modeAuto_active':
                return ClimateStatePayload(
                    climate_state_type=ClimateStatePayloadTypeEnum.CLIMATE_MODE,
                    command=ClimateCommandsEnum.SET_CLIMATE_MODE_AUTO,
                    value=True
                )
            case 'modeDry_active':
                return ClimateStatePayload(
                    climate_state_type=ClimateStatePayloadTypeEnum.CLIMATE_MODE,
                    command=ClimateCommandsEnum.SET_CLIMATE_MODE_DRY,
                    value=True
                )
            case 'modeFan_active':
                return ClimateStatePayload(
                    climate_state_type=ClimateStatePayloadTypeEnum.CLIMATE_MODE,
                    command=ClimateCommandsEnum.SET_CLIMATE_MODE_FAN,
                    value=True
                )
            # FAN
            case 'fanSpeedM3V3_active':
                return ClimateStatePayload(
                    climate_state_type=ClimateStatePayloadTypeEnum.FAN_SPEED,
                    command=ClimateCommandsEnum.SET_FAN_SPEED,
                    value=3
                )
            case 'fanSpeedM3V2_active':
                return ClimateStatePayload(
                    climate_state_type=ClimateStatePayloadTypeEnum.FAN_SPEED,
                    command=ClimateCommandsEnum.SET_FAN_SPEED,
                    value=2
                )
            case 'fanSpeedM3V1_active':
                return ClimateStatePayload(
                    climate_state_type=ClimateStatePayloadTypeEnum.FAN_SPEED,
                    command=ClimateCommandsEnum.SET_FAN_SPEED,
                    value=1
                )
            case 'fanSpeedAuto_active':
                return ClimateStatePayload(
                    climate_state_type=ClimateStatePayloadTypeEnum.FAN_SPEED,
                    command=ClimateCommandsEnum.SET_CLIMATE_MODE_AUTO,
                    value=True
                )

            # OPTIONS FUNC
            case 'extMute_active':
                return ClimateStatePayload(
                    climate_state_type=ClimateStatePayloadTypeEnum.OPTION_FUNCTION,
                    command=ClimateCommandsEnum.FUNC_MUTE_SOUND,
                    value=True
                )
            case 'extTurbo_active':
                return ClimateStatePayload(
                    climate_state_type=ClimateStatePayloadTypeEnum.OPTION_FUNCTION,
                    command=ClimateCommandsEnum.FUNC_TURBO,
                    value=True
                )
            case 'extEconomy_active':
                return ClimateStatePayload(
                    climate_state_type=ClimateStatePayloadTypeEnum.OPTION_FUNCTION,
                    command=ClimateCommandsEnum.FUNC_ECO,
                    value=True
                )
            case 'flowHorizontOn_active':
                return ClimateStatePayload(
                    climate_state_type=ClimateStatePayloadTypeEnum.OPTION_FUNCTION,
                    command=ClimateCommandsEnum.FUNC_HORIZONT_SWING,
                    value=True
                )
            case 'flowVertOn_active':
                return ClimateStatePayload(
                    climate_state_type=ClimateStatePayloadTypeEnum.OPTION_FUNCTION,
                    command=ClimateCommandsEnum.FUNC_VERTICAL_SWING,
                    value=True
                )

        # SET TEMP
        if self.text is not None:
            if '°C' in self.text:
                set_temp = self.text.replace('°C', '').strip()
                return ClimateStatePayload(
                    climate_state_type=ClimateStatePayloadTypeEnum.SET_TEMP_C,
                    command=ClimateCommandsEnum.SET_TEMP,
                    value=int(set_temp)
                )
            if '°F' in self.text:
                set_temp = self.text.replace('°C', '').strip()
                return ClimateStatePayload(
                    climate_state_type=ClimateStatePayloadTypeEnum.SET_TEMP_F,
                    command=ClimateCommandsEnum.SET_TEMP,
                    value=int(set_temp)
                )

        return None

class PlaceState(BaseModel):
    """
        conditioner current state, status about power
    """
    is_on: Optional[bool] = Field(None, alias="isOn") # True - is On, False - is Off
    details: Optional[List[PlaceDetailItem]] = Field(default_factory=list, alias='details')

    @field_validator("details", mode="before")
    @classmethod
    def id_strip_prefix(cls, value):
        """
            fixing the nesting level
        """
        if len(value) > 0:
            if 'details' in value[0]:
                return value[0]['details']
        return value


class Place(BaseModel):
    id: int # id device for control
    title: str # Name specified by the owner like "Living room", "Bedroom 2th floor"
    serial: str
    access: Optional[AccessEnum] = None
    status: Optional[PlaceStatusEnum] = None
    state: Optional[PlaceState]
    building_id: Optional[int] = Field(None, alias="buildingId")
    cloud_type: Optional[str] = Field(None, alias="cloudType")
    firmware_type: Optional[str] = Field(None, alias="firmwareType")
    sensor_temp: Optional[int] = Field(None, alias="curTemp")
    firmware_type: Optional[str] = Field(None, alias="firmwareType")

    @root_validator(pre=True)
    def parse_text_to_payload(cls, values):
        pprint(values)
        return values


class Building(BaseModel):
    id: int
    access: Optional[AccessEnum] = None
    title: str
    utc: int
    address: Optional[str]
    timeZone: str
    paces: List[Place] = Field(default_factory=list, alias='places')
