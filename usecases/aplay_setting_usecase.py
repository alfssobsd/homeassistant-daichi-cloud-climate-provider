from dataproviders.daichicloud.daichicloud_api import DaichiCloudClient


class AplaySettingUseCase:
    """
        Looking for device and publish to homeassistant
    """

    def __init__(self, daichi: DaichiCloudClient):
        self.daichi = daichi

    def execute(self, filter: str):
        pass