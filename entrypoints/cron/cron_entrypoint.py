from datetime import datetime, timedelta

import schedule
import structlog

from usecases.discovery_usecase import DiscoveryClimateDeviceUseCase

log = structlog.get_logger()


class CronEntrypoints:

    def __init__(self, discovery_climate_uc: DiscoveryClimateDeviceUseCase, auto_discovery_minutes: int = 30):
        self.discovery_climate_uc = discovery_climate_uc
        self.auto_discovery_minutes = auto_discovery_minutes

    def start_cron(self):
        log.info(f'Setup auto-discovery every {self.auto_discovery_minutes} minutes')
        self.task_auto_discovery = schedule.every(self.auto_discovery_minutes).minutes.do(
            self.periodic_discovery_devices_and_restore_state)

        log.info(f'Force run on start in 2 seconds')
        self.task_auto_discovery.next_run = datetime.now() + timedelta(seconds=2)

    def periodic_discovery_devices_and_restore_state(self):
        log.info('Looking for devices or update state...')
        self.discovery_climate_uc.execute()
