from json import JSONDecodeError

import requests
import random

from dataproviders.daichicloud.command_registry import ClimateCommandsEnum, ClimateCommandFunctionTypeEnum
from dataproviders.daichicloud.dto import UserData, Building, ControlRequest, ControlSetValueRequest, ControlResponse, \
    ControlOnOffValueRequest
from dataproviders.daichicloud.exceptions import DaichiCloudException, DaichiCloudUnknowErrorException, \
    DaichiCloudServerProblemException, DaichiCloudAuthErrorException, DaichiCloudCommandException

_DAICHI_MIN_RAND = 1
_DAICHI_MAX_RAND = 99999999


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
        self.sysrand = random.SystemRandom()

    def __exception_if_get_errors(self, status_code: int, response_text: str | None):
        if status_code in [503, 504, 500]:
            raise DaichiCloudServerProblemException(f"Response: {response_text}", status_code)
        if status_code in [401, 403]:
            raise DaichiCloudAuthErrorException(f"Error auth or access denied: {response_text}", status_code)
        if status_code != 200:
            raise DaichiCloudUnknowErrorException(f"Response: {response_text}", status_code)

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def _get_token(self):
        """
        Use username and password for get Bearer token
        :return: Bearer <token>
        """
        url = f"{self.base_url}/token"
        payload = {
            "grant_type": "password",
            "email": self.username,
            "password": self.password,
            "clientId": self.client_id
        }
        response = requests.post(url, json=payload)

        self.__exception_if_get_errors(status_code=response.status_code, response_text=response.text)

        try:
            data = response.json()
        except JSONDecodeError:
            raise DaichiCloudAuthErrorException(message=f"Error format or incorrect login/password",
                                                code=response.status_code)

        if not data.get("done", False):
            raise DaichiCloudAuthErrorException(message=f"Error format: {data}", code=response.status_code)

        access_token = data.get("data", {}).get("access_token")
        if not access_token:
            raise DaichiCloudException("No token received")

        return access_token

    def refresh_token(self):
        """
        Refresh access token
        :return: None
        """
        self.access_token = self._get_token()

    def get_userinfo(self) -> UserData:
        """
        Get information about user and mqtt credentials
        :return: UserData
        """
        url = f"{self.base_url}/user"
        response = requests.get(url, headers=self._get_headers())
        self.__exception_if_get_errors(status_code=response.status_code, response_text=response.text)

        try:
            data = response.json()
        except JSONDecodeError:
            raise DaichiCloudAuthErrorException(message=f"Error format or incorrect login/password",
                                                code=response.status_code)

        userinfo = UserData.model_validate(data['data'])
        return userinfo

    def get_buildings(self) -> list[Building]:
        """
        Get information buildings and places. place equal climate device
        :return: list[Building]
        """
        url = f"{self.base_url}/buildings"

        response = requests.get(url, headers=self._get_headers())
        self.__exception_if_get_errors(status_code=response.status_code, response_text=response.text)

        try:
            data = response.json()
        except JSONDecodeError:
            raise DaichiCloudAuthErrorException(message=f"Error format or incorrect login/password",
                                                code=response.status_code)

        buildings = [Building.model_validate(item) for item in data['data']]

        return buildings

    def execute_command(self, device_id: int, command: ClimateCommandsEnum, payload: bool | int) -> ControlResponse:
        """
        Execute command in Dachi Cloud for control climate devices
        :return: ControlResponse
        :raises DaichiCloudApiException: - if api has error auth key or other
        """
        compile_api_path = f'{self.base_url}/{command.value.api_path.format(device_id=device_id)}'
        match command.value.function_type:
            case ClimateCommandFunctionTypeEnum.ON_OFF:
                if payload not in command.value.available_value:
                    raise DaichiCloudCommandException(f"Not in available_value={command.value.available_value}")

                command_payload = ControlRequest(
                    cmd_id=self.sysrand.randint(_DAICHI_MIN_RAND, _DAICHI_MAX_RAND),
                    value=ControlOnOffValueRequest(
                        function_id=command.value.function_id,
                        is_on=payload,
                        parameters=None
                    ),
                    conflict_resolve_data=None
                )
            case ClimateCommandFunctionTypeEnum.MIN_MAX:
                min_value = command.value.available_value[0]
                max_value = command.value.available_value[1]
                if payload < min_value or payload > max_value:
                    raise DaichiCloudCommandException(f"Out of available range min={min_value} max={max_value}")

                command_payload = ControlRequest(
                    cmd_id=self.sysrand.randint(_DAICHI_MIN_RAND, _DAICHI_MAX_RAND),
                    value=ControlSetValueRequest(
                        function_id=command.value.function_id,
                        value=payload,
                        parameters=None
                    ),
                    conflict_resolve_data=None
                )
            case _:  # ClimateCommandFunctionTypeEnum.INT_VALUE
                if payload not in command.value.available_value:
                    raise DaichiCloudCommandException(f"Not in available_value={command.value.available_value}")

                command_payload = ControlRequest(
                    cmd_id=self.sysrand.randint(_DAICHI_MIN_RAND, _DAICHI_MAX_RAND),
                    value=ControlSetValueRequest(
                        function_id=command.value.function_id,
                        value=payload,
                        parameters=None
                    ),
                    conflict_resolve_data=None
                )

        response = requests.post(compile_api_path, headers=self._get_headers(),
                                 json=command_payload.model_dump(by_alias=True))
        self.__exception_if_get_errors(status_code=response.status_code, response_text=response.text)

        try:
            data = response.json()
        except JSONDecodeError:
            raise DaichiCloudAuthErrorException(message=f"Error format or incorrect login/password",
                                                code=response.status_code)

        return ControlResponse.model_validate(data)

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
