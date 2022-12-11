from typing import Any, Optional

from app.enum import PortStatus, Protocol
from app.schemes.base import CamelModel


class Service(CamelModel):
    port: int
    status: PortStatus = PortStatus.open
    name: Optional[str] = None
    proto: Protocol = Protocol.tcp
    product: Optional[str] = None
    version: Optional[str] = None
    meta: dict[str, Any]


class ServiceORM(Service):
    id: int

    class Config:
        orm_mode = True
