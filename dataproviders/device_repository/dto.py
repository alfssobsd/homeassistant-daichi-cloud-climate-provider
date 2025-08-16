from pydantic import BaseModel


class ClimateDeviceEntity(BaseModel):
    # DAICHI CLOUD DEVICE ID
    climate_device_id: int

    # Mode
    mode_state: str = None
    # daichi_cloud_climate/device_id_xxxxx/ac/mode/state
    mode_state_topic: str

    # Fan
    fan_mode_state: str = None
    # daichi_cloud_climate/device_id_xxxxx/ac/fan/state
    fan_mode_state_topic: str

    # Temperature state
    temperature_state: int = None
    # daichi_cloud_climate/device_id_xxxxx/ac/temperature/state
    temperature_state_topic: str

    # Current Temperature
    # daichi_cloud_climate/device_id_xxxxx/ac/temperature_curr/state
    current_temperature_topic: str
    # Current Temperature state
    current_temperature_state: int = None

    # ClimateCommandsEnum.FUNC_MUTE_SOUND = True
    enable_mute_sound: bool