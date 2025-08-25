from datetime import datetime, timedelta

import schedule
import structlog

from usecases.discovery_usecase import DiscoveryClimateDeviceUseCase

log = structlog.get_logger()


class CronEntrypoint:

    def __init__(self, discovery_climate_uc: DiscoveryClimateDeviceUseCase, discovery_interval_minutes: int = 30):
        self.discovery_climate_uc = discovery_climate_uc
        self.discovery_interval_minutes = discovery_interval_minutes
        log.info(f'Discovery interval {discovery_interval_minutes} minutes')

    def setup_cron(self):
        log.info(f'Setup auto-discovery every {self.discovery_interval_minutes} minutes')
        self.task_auto_discovery = schedule.every(self.discovery_interval_minutes).minutes.do(
            self.periodic_discovery_devices_and_restore_state)

        log.info(f'Force run on start in 2 seconds')
        self.task_auto_discovery.next_run = datetime.now() + timedelta(seconds=2)

    def periodic_discovery_devices_and_restore_state(self):
        log.info('Looking for devices or update state...')
        self.discovery_climate_uc.execute()
        # raise Exception("BUMP")
