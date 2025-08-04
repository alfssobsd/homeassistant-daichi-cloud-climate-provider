from dataclasses import dataclass
from enum import Enum


class ClimateCommandValueTypeEnum(Enum):
    ON_OFF = 1
    INT_VALUE = 2
    MIN_MAX = 3


@dataclass(frozen=True)
class ClimateCommandDescribe:
    function_id: int
    function_type: ClimateCommandValueTypeEnum
    available_value: list


class ClimateCommandsEnum(Enum):
    POWER = ClimateCommandDescribe(function_id=334,
                                   function_type=ClimateCommandValueTypeEnum.ON_OFF,
                                   available_value=[True, False])
    SET_CLIMATE_MODE_COOL = ClimateCommandDescribe(function_id=336,
                                                   function_type=ClimateCommandValueTypeEnum.ON_OFF,
                                                   available_value=[True])
    SET_CLIMATE_MODE_HEAT = ClimateCommandDescribe(function_id=337,
                                                   function_type=ClimateCommandValueTypeEnum.ON_OFF,
                                                   available_value=[True])
    SET_CLIMATE_MODE_AUTO = ClimateCommandDescribe(function_id=338,
                                                   function_type=ClimateCommandValueTypeEnum.ON_OFF,
                                                   available_value=[True])
    SET_CLIMATE_MODE_DRY = ClimateCommandDescribe(function_id=339,
                                                  function_type=ClimateCommandValueTypeEnum.ON_OFF,
                                                  available_value=[True])
    SET_CLIMATE_MODE_FAN = ClimateCommandDescribe(function_id=340,
                                                  function_type=ClimateCommandValueTypeEnum.ON_OFF,
                                                  available_value=[True])
    SET_FAN_SPEED = ClimateCommandDescribe(function_id=342,
                                           function_type=ClimateCommandValueTypeEnum.INT_VALUE,
                                           available_value=[1, 2, 3])
    SET_FAN_SPEED_AUTO = ClimateCommandDescribe(function_id=341,
                                                function_type=ClimateCommandValueTypeEnum.ON_OFF,
                                                available_value=[True])
    SET_TEMP = ClimateCommandDescribe(function_id=335,
                                      function_type=ClimateCommandValueTypeEnum.MIN_MAX,
                                      available_value=[17, 32])
    FUNC_MUTE_SOUND = ClimateCommandDescribe(function_id=347,
                                             function_type=ClimateCommandValueTypeEnum.ON_OFF,
                                             available_value=[True, False])
    FUNC_TURBO = ClimateCommandDescribe(function_id=346,
                                        function_type=ClimateCommandValueTypeEnum.ON_OFF,
                                        available_value=[True, False])
    FUNC_ECO = ClimateCommandDescribe(function_id=345,
                                      function_type=ClimateCommandValueTypeEnum.ON_OFF,
                                      available_value=[True, False])
    FUNC_HORIZONT_SWING = ClimateCommandDescribe(function_id=348,
                                                 function_type=ClimateCommandValueTypeEnum.ON_OFF,
                                                 available_value=[True, False])
    FUNC_VERTICAL_SWING = ClimateCommandDescribe(function_id=343,
                                                 function_type=ClimateCommandValueTypeEnum.ON_OFF,
                                                 available_value=[True, False])
