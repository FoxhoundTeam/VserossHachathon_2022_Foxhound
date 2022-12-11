from typing import TYPE_CHECKING

from sqlalchemy import ARRAY, Column, Float, String
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship

from app.database.article_cluster import article_cluster
from app.database.base import Base

if TYPE_CHECKING:
    from app.database import Article


class Cluster(Base):
    """Кластер."""

    theme: list[str] = Column(MutableList.as_mutable(ARRAY(String)), nullable=False, default=[])
    class_name: str = Column(String, nullable=False)
    location: str = Column(String, nullable=False)
    lat: float = Column(Float, nullable=False)
    lon: float = Column(Float, nullable=False)
    articles: list["Article"] = relationship(
        "Article", secondary=article_cluster, back_populates="clusters", passive_deletes=True
    )
