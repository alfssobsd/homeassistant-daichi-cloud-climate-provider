import threading
from dataproviders.device_repository.dto import ClimateDeviceEntity


class ClimateDeviceRepository:
    _REPO_DEVICE_LIST: dict[int, ClimateDeviceEntity]

    def __init__(self):
        self._REPO_DEVICE_LIST = dict()
        self._lock = threading.Lock()

    def set_device(self, climate_device: ClimateDeviceEntity):
        with self._lock:
            self._REPO_DEVICE_LIST[climate_device.climate_device_id] = climate_device

    def get_by_id(self, climate_device_id: int) -> ClimateDeviceEntity | None:
        with self._lock:
            if climate_device_id in self._REPO_DEVICE_LIST.keys():
                return self._REPO_DEVICE_LIST[climate_device_id]
        return None
