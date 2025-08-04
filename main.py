from dataproviders.daichicloud.daichicloud_api import DaichiCloudClient


def main():
    rrr = DaichiCloudClient(

    )
    rrr.get_userinfo()
    rrr.get_buildings()
    # print(rrr.get_mqtt_topic_notification())
    # print(rrr.get_mqtt_topic_commands_status())

if __name__ == "__main__":
    main()