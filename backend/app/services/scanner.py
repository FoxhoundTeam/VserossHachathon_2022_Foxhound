from dataclasses import dataclass
from functools import cached_property

from sqlalchemy.orm import Session

from app import schemes
from app.database import Scan, Service
from app.enum import ScanStatus
from app.services.brute_psql import BrutePSQL
from app.services.masscan import MasscanService
from app.services.nmap import NmapService


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
            self.scan.progress = initial_progress + progress / 2
            self.scan.log += logs + "\n"
            self.session.add(self.scan)
            self.session.commit()

        return _handle_progress_logs

    def start(self):
        try:
            masscan_result = MasscanService(self.scan.ip, self._get_progress_logs_handler()).start_scan()
            nmap_result = NmapService(
                self.scan.ip, ",".join([str(service.port) for service in masscan_result])
            ).start_scan()
            filled_services = BrutePSQL(self.scan.ip, nmap_result).brute()
            self._save_services(filled_services)
        except Exception as e:
            self.scan.log += f"{e}\n"
            self.scan.status = ScanStatus.error
            self.session.add(self.scan)
            self.session.commit()
