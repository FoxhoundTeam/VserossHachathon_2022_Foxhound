from ipaddress import IPv4Address

from app.database import Scan
from app.services.base import BaseDBService
from app.tasks import start_scan
from app.utils import get_or_404


class ScanService(BaseDBService):
    def all_query(self):
        return self.session.query(Scan)

    def get(self, id_: int) -> Scan:
        return get_or_404(self.session, Scan, id_, "Скан не найден")

    def start_scan(self, ip: IPv4Address) -> Scan:
        scan = Scan(ip=ip)
        self._save_obj(scan)
        start_scan.send(scan.id)
        return scan
