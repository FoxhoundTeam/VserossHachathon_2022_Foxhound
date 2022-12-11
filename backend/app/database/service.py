from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.enum import PortStatus, Protocol

if TYPE_CHECKING:
    from app.database import Scan


class Service(Base):
    """Сервис."""

    port: int = Column(Integer, nullable=False)
    status: PortStatus = Column(String, nullable=False)
    name: str = Column(String)
    proto: Protocol = Column(String, nullable=False)
    product: str = Column(String)
    version: str = Column(String)
    meta: dict[str, Any] = Column(JSON, default=dict)
    scan_id: int = Column(Integer, ForeignKey("scan.id"))
    scan: "Scan" = relationship("Scan", back_populates="services")
