from typing import Optional

from pydantic import BaseModel, computed_field


class DeviceClimateDeviceDescribe(BaseModel):
    serial_number: Optional[str]


class DeviceClimateDescribe(BaseModel):
    original_dachi_cloud_id: int
    name: str
    min_temp: int
    max_temp: int
    device: DeviceClimateDeviceDescribe

    @computed_field
    def unique_id(self) -> str:
        return f'dachi_cloud_{self.original_dachi_cloud_id}'

    @computed_field
    def payload_on(self) -> str:
        return 'ON'

    @computed_field
    def payload_off(self) -> str:
        return 'OFF'

    #### modes
    @computed_field
    def modes(self) -> list:
        return ["off", "cool", "heat", "auto", "fan_only", "dry"]

    @computed_field
    def mode_command_topic(self) -> str:
        return f'dachi_cloud_climate/{self.unique_id}/ac/mode/set'

    @computed_field
    def mode_state_topic(self) -> str:
        return f'dachi_cloud_climate/{self.unique_id}/ac/mode/state'

    #### fans
    @computed_field
    def fan_modes(self) -> list:
        return ["auto", "low", "medium", "high"]

    @computed_field
    def fan_mode_command_topic(self) -> str:
        return f'dachi_cloud_climate/{self.unique_id}/ac/fan/set'

    @computed_field
    def fan_mode_state_topic(self) -> str:
        return f'dachi_cloud_climate/{self.unique_id}/ac/fan/state'

    #### temperature
    @computed_field
    def temperature_command_topic(self) -> str:
        return f'dachi_cloud_climate/{self.unique_id}/ac/temperature/set'

    @computed_field
    def temperature_state_topic(self) -> str:
        return f'dachi_cloud_climate/{self.unique_id}/ac/temperature/state'

    def discovery_device_climate_topic(self) -> str:
        return f'homeassistant/climate/{self.unique_id}/climate/config'
