from dataclasses import dataclass
from functools import cached_property
from typing import Type

from sqlalchemy.orm import Session

from app import schemes
from app.database import Scan, Service
from app.enum import ScanStatus
from app.services.scanner.base_stage import BaseStage
from app.services.scanner.brute_psql import BrutePSQLService
from app.services.scanner.masscan import MasscanService
from app.services.scanner.nmap import NmapService

PIPELINE: list[Type[BaseStage]] = [
    MasscanService,
    NmapService,
    BrutePSQLService,
]


@dataclass
class Scanner:
    session: Session
    scan_id: int

    @cached_property
    def scan(self) -> Scan:
        return self.session.query(Scan).filter(Scan.id == self.scan_id).first()

    def _save_services(self, services: list[schemes.Service]):
        self.session.add_all([Service(scan=self.scan, **service.dict()) for service in services])
        self.scan.progress = 1
        self.scan.status = ScanStatus.finished
        self.session.add(self.scan)
        self.session.commit()

    def _get_progress_logs_handler(self):
        initial_progress = self.scan.progress

        def _handle_progress_logs(logs: str, progress: float):
            self.scan.progress = initial_progress + progress / len(PIPELINE)
            if logs:
                self.scan.log += logs + "\n"
            self.session.add(self.scan)
            self.session.commit()

        return _handle_progress_logs

    def start(self):
        try:
            services = None
            for stage in PIPELINE:
                if services is None:
                    services = stage(self.scan.ip, self._get_progress_logs_handler()).start()
                else:
                    services = stage(self.scan.ip, services, self._get_progress_logs_handler()).start()
            self._save_services(services)
        except Exception as e:
            self.scan.log += f"{e}\n"
            self.scan.status = ScanStatus.error
            self.session.add(self.scan)
            self.session.commit()
