from dataclasses import dataclass
from enum import Enum


class ClimateCommandFunctionTypeEnum(Enum):
    ON_OFF = 1
    INT_VALUE = 2
    MIN_MAX = 3


@dataclass(frozen=True)
class ClimateCommandDescribe:
    function_id: int
    function_type: ClimateCommandFunctionTypeEnum
    available_value: list
    api_path: str
    should_power_on: bool = True


class ClimateCommandsEnum(Enum):
    POWER = ClimateCommandDescribe(function_id=334,
                                   function_type=ClimateCommandFunctionTypeEnum.ON_OFF,
                                   available_value=[True, False],
                                   api_path="devices/{device_id}/ctrl?ignoreConflicts=false")
    SET_CLIMATE_MODE_COOL = ClimateCommandDescribe(function_id=336,
                                                   function_type=ClimateCommandFunctionTypeEnum.ON_OFF,
                                                   available_value=[True],
                                                   api_path="devices/{device_id}/ctrl?ignoreConflicts=false")
    SET_CLIMATE_MODE_HEAT = ClimateCommandDescribe(function_id=337,
                                                   function_type=ClimateCommandFunctionTypeEnum.ON_OFF,
                                                   available_value=[True],
                                                   api_path="devices/{device_id}/ctrl?ignoreConflicts=false")
    SET_CLIMATE_MODE_AUTO = ClimateCommandDescribe(function_id=338,
                                                   function_type=ClimateCommandFunctionTypeEnum.ON_OFF,
                                                   available_value=[True],
                                                   api_path="devices/{device_id}/ctrl?ignoreConflicts=false")
    SET_CLIMATE_MODE_DRY = ClimateCommandDescribe(function_id=339,
                                                  function_type=ClimateCommandFunctionTypeEnum.ON_OFF,
                                                  available_value=[True],
                                                  api_path="devices/{device_id}/ctrl?ignoreConflicts=false")
    SET_CLIMATE_MODE_FAN = ClimateCommandDescribe(function_id=340,
                                                  function_type=ClimateCommandFunctionTypeEnum.ON_OFF,
                                                  available_value=[True],
                                                  api_path="devices/{device_id}/ctrl?ignoreConflicts=false")
    SET_FAN_SPEED = ClimateCommandDescribe(function_id=342,
                                           function_type=ClimateCommandFunctionTypeEnum.INT_VALUE,
                                           available_value=[1, 2, 3],
                                           api_path="devices/{device_id}/ctrl?ignoreConflicts=false")
    SET_FAN_SPEED_AUTO = ClimateCommandDescribe(function_id=341,
                                                function_type=ClimateCommandFunctionTypeEnum.ON_OFF,
                                                available_value=[True],
                                                api_path="devices/{device_id}/ctrl?ignoreConflicts=false")
    SET_TEMP = ClimateCommandDescribe(function_id=335,
                                      function_type=ClimateCommandFunctionTypeEnum.MIN_MAX,
                                      available_value=[17, 32],
                                      api_path="devices/{device_id}/ctrl?ignoreConflicts=false")
    FUNC_MUTE_SOUND = ClimateCommandDescribe(function_id=347,
                                             function_type=ClimateCommandFunctionTypeEnum.ON_OFF,
                                             available_value=[True, False],
                                             api_path="devices/{device_id}/ctrl?ignoreConflicts=false",
                                             should_power_on=False)
    FUNC_TURBO = ClimateCommandDescribe(function_id=346,
                                        function_type=ClimateCommandFunctionTypeEnum.ON_OFF,
                                        available_value=[True, False],
                                        api_path="devices/{device_id}/ctrl?ignoreConflicts=false")
    FUNC_ECO = ClimateCommandDescribe(function_id=345,
                                      function_type=ClimateCommandFunctionTypeEnum.ON_OFF,
                                      available_value=[True, False],
                                      api_path="devices/{device_id}/ctrl?ignoreConflicts=false")
    FUNC_HORIZONT_SWING = ClimateCommandDescribe(function_id=348,
                                                 function_type=ClimateCommandFunctionTypeEnum.ON_OFF,
                                                 available_value=[True, False],
                                                 api_path="devices/{device_id}/ctrl?ignoreConflicts=false")
    FUNC_VERTICAL_SWING = ClimateCommandDescribe(function_id=343,
                                                 function_type=ClimateCommandFunctionTypeEnum.ON_OFF,
                                                 available_value=[True, False],
                                                 api_path="devices/{device_id}/ctrl?ignoreConflicts=false")
