from typing import TYPE_CHECKING

from sqlalchemy import ARRAY, Column, Float, String
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship
from sqlalchemy_utils import IPAddressType

from app.database.base import Base
from app.enum import ScanStatus

if TYPE_CHECKING:
    from ipaddress import IPv4Address

    from app.database import Service


class Scan(Base):
    """Сканирование."""

    ip: "IPv4Address" = Column(IPAddressType, nullable=False)
    status: ScanStatus = Column(String, nullable=False, default=ScanStatus.running)
    log: list[str] = Column(MutableList.as_mutable(ARRAY(String)), nullable=False, default=[])
    progress: float = Column(Float, default=0, nullable=False)
    services: list["Service"] = relationship("Service", back_populates="scan")
