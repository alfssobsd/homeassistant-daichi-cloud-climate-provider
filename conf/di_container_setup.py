from dependency_injector import containers, providers
from pydantic.v1 import BaseModel, Field

from dataproviders.daichicloud.daichicloud_api import DaichiCloudClient
from dataproviders.device_repository.device_repo import ClimateDeviceRepository
from dataproviders.homeassistant_mqtt.mqtt_provider import HomeAssistantMQTTClimateProvider
from entrypoints.cron.cron_entrypoint import CronEntrypoint
from entrypoints.mqtt.mqtt_entrypoint import HomeAssistantMQTTEntrypoint
from usecases.apply_commands_usecase import ApplyCommandsUseCase
from usecases.discovery_usecase import DiscoveryClimateDeviceUseCase
from usecases.restore_state_usecase import RestoreStateClimateDeviceUseCase


class AppConfig(BaseModel):
    DAICHI_USER: str = Field(..., alias="DAICHI_USER")
    DAICHI_PASS: str = Field(..., alias="DAICHI_PASS")
    MQTT_HOST: str = Field(..., alias="MQTT_HOST")
    MQTT_PORT: int = Field(..., alias="MQTT_PORT")
    MQTT_USER: str = Field(..., alias="MQTT_USER")
    MQTT_PASS: str = Field(..., alias="MQTT_PASS")
    APP_ENABLE_MUTE_SOUND: bool = Field(..., alias="APP_ENABLE_MUTE_SOUND")
    APP_DISCOVERY_INTERVAL_MINUTES: int = Field(30, alias="APP_DISCOVERY_INTERVAL_MINUTES")
    APP_FILTER_BUILDINGS: str = Field('', alias="APP_FILTER_BUILDINGS")
    APP_FILTER_PLACES: str = Field('', alias="APP_FILTER_PLACES")


class Container(containers.DeclarativeContainer):
    # config = providers.Configuration()

    config = providers.Singleton(
        AppConfig
    )
    # API DAICHI
    daichi_cloud_client = providers.Singleton(
        DaichiCloudClient,
        username=providers.Callable(lambda cfg: cfg.DAICHI_USER, config),
        password=providers.Callable(lambda cfg: cfg.DAICHI_PASS, config),
    )

    # MQTT
    mqtt_provider = providers.Singleton(
        HomeAssistantMQTTClimateProvider,
        host=providers.Callable(lambda cfg: cfg.MQTT_HOST, config),
        port=providers.Callable(lambda cfg: cfg.MQTT_PORT, config),
        username=providers.Callable(lambda cfg: cfg.MQTT_USER, config),
        password=providers.Callable(lambda cfg: cfg.MQTT_PASS, config),
    )

    # Repo
    climate_device_repo = providers.Singleton(
        ClimateDeviceRepository,
    )

    # UseCases
    restore_state_uc = providers.Factory(
        RestoreStateClimateDeviceUseCase,
        mqtt_provider=mqtt_provider,
        climate_device_repo=climate_device_repo,
    )

    apply_commands_uc = providers.Factory(
        ApplyCommandsUseCase,
        daichi=daichi_cloud_client,
        restore_state_uc=restore_state_uc,
        climate_device_repo=climate_device_repo,
        mqtt_provider=mqtt_provider,
        enable_silence_mode=providers.Callable(lambda cfg: cfg.APP_ENABLE_MUTE_SOUND, config),
    )

    discovery_climate_uc = providers.Factory(
        DiscoveryClimateDeviceUseCase,
        daichi=daichi_cloud_client,
        climate_device_repo=climate_device_repo,
        mqtt_provider=mqtt_provider,
        restore_state_uc=restore_state_uc,
        buildings_filter=providers.Callable(lambda cfg: cfg.APP_FILTER_BUILDINGS, config),
        places_filter=providers.Callable(lambda cfg: cfg.APP_FILTER_PLACES, config),
    )

    # Entrypoints
    mqtt_entrypoint = providers.Singleton(
        HomeAssistantMQTTEntrypoint,
        apply_commands_uc=apply_commands_uc
    )

    cron_entrypoint = providers.Singleton(
        CronEntrypoint,
        discovery_climate_uc=discovery_climate_uc,
        discovery_interval_minutes=providers.Callable(lambda cfg: cfg.APP_DISCOVERY_INTERVAL_MINUTES, config),
    )
