from ipaddress import IPv4Address

from pydantic import validator

from app.config import settings
from app.enum import ScanStatus
from app.schemes.base import CamelModel


class ScanCreate(CamelModel):
    ip: IPv4Address

    @validator("ip")
    def check_ip_allowed(cls, v: IPv4Address):
        if not settings.allow_scan_any_ip and str(v) != "158.160.43.251":
            raise ValueError("Сканирование данного адреса запрещено.")
        return v


class ScanORM(CamelModel):
    id: int
    status: ScanStatus
    ip: IPv4Address
    log: list[str]
    progress: float

    class Config:
        orm_mode = True
