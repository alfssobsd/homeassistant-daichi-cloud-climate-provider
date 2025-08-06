import os.path

from dotenv import load_dotenv

from dataproviders.daichicloud.command_registry import ClimateCommandsEnum
from dataproviders.daichicloud.daichicloud_api import DaichiCloudClient


def main():
    if os.path.exists('.env'):
        load_dotenv()

    # print(os.getenv('DAICHI_USER'))
    rrr = DaichiCloudClient(
        username=os.getenv('DAICHI_USER'),
        password=os.getenv('DAICHI_PASS')
    )
    # rrr.get_userinfo()
    # rrr.get_buildings()
    print(rrr.execute_command(device_id=287369, command=ClimateCommandsEnum.SET_FAN_SPEED, payload=2))

    # print(rrr.get_mqtt_topic_notification())
    # print(rrr.get_mqtt_topic_commands_status())

if __name__ == "__main__":
    main()