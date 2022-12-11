from ipaddress import IPv4Address

from app.enum import ScanStatus
from app.schemes.base import CamelModel


class ScanCreate(CamelModel):
    ip: IPv4Address


class ScanORM(ScanCreate):
    id: int
    status: ScanStatus
    log: list[str]
    progress: float

    class Config:
        orm_mode = True
