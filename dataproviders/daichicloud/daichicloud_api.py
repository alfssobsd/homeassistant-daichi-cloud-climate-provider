import requests

from dataproviders.daichicloud.dto import UserData, Building
from dataproviders.daichicloud.exceptions import DaichiCloudApiException, DaichiCloudException


# TODO: нужно сделать конкретное решение для кондеев и опубликовать, пусть будет
#  отдельной прогой и не будет скрещиваться с другим, а кому-топ пригодится дальше

class DaichiCloudClient:
    def __init__(self, username, password,
                 base_url="https://web.daichicloud.ru/api/v4",
                 client_id='sOJO7B6SqgaKudTfCzqLAy540cCuDzpI',
                 mqtt_url='wss://split.daichicloud.ru/mqtt'):
        """
        """
        self.username = username
        self.password = password
        self.base_url = base_url
        self.mqtt_url = mqtt_url
        self.client_id = client_id
        self.access_token = self._get_token()
        self.user_info: UserData = self.get_userinfo()

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def _get_token(self):
        url = f"{self.base_url}/token"
        payload = {
            "grant_type": "password",
            "email": self.username,
            "password": self.password,
            "clientId": self.client_id
        }
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            raise DaichiCloudApiException(f"Error getting token: {response.text}", code=response.status_code)
        data = response.json()

        if not data.get("done", False):
            raise DaichiCloudException(f"API error: {data.get('message', 'Unknown error')}")

        access_token = data.get("data", {}).get("access_token")
        if not access_token:
            raise DaichiCloudException("No token received")

        return access_token

    def get_userinfo(self) -> UserData:
        url = f"{self.base_url}/user"
        response = requests.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise DaichiCloudApiException(f"Error get user: {response.text}", response.status_code)
        data = response.json()

        userinfo = UserData.model_validate(data['data'])
        return userinfo

    def get_buildings(self) -> list[Building]:
        url = f"{self.base_url}/buildings"

        response = requests.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise DaichiCloudApiException(f"Error get user: {response.text}", response.status_code)
        data = response.json()

        buildings = [Building.model_validate(item) for item in data['data']]
        return buildings

    def get_mqtt_topic_notification(self):
        """
        Get path to MQTT topic for user - notification
        'user/${user_id}/notification'

        Before please get_userinfo for get username and password mqtt credentials
        fields mqtt_credentials.username and mqtt_credentials.password


        :return: path to mqtt topic notification
        """
        return f"{self.mqtt_url}/{self.user_info.id}/notification"

    def get_mqtt_topic_pre_notification(self):
        """
        Get path to MQTT topic for user - pre-notification
        'user/${user_id}/pre-notification'

        Before please get_userinfo for get username and password mqtt credentials
        fields mqtt_credentials.username and mqtt_credentials.password


        :return: path to mqtt topic pre-notification
        """
        return f"{self.mqtt_url}/{self.user_info.id}/pre-notification"

    def get_mqtt_topic_commands_status(self):
        """
        Get path to MQTT topic for user - pre-notification
        'user/${user_id}/pre-notification'

        Before please get_userinfo for get username and password mqtt credentials
        fields mqtt_credentials.username and mqtt_credentials.password

        :return: path to mqtt topic status of commands
        """
        return f"{self.mqtt_url}/{self.user_info.id}/out/control/commands/status"