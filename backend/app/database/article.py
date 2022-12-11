from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Column, Date, String
from sqlalchemy.orm import relationship

from app.database.article_cluster import article_cluster
from app.database.base import Base

if TYPE_CHECKING:
    from app.database import Cluster


class Article(Base):
    """Статья."""

    url: str = Column(String)
    title: str = Column(String, nullable=False)
    text: str = Column(String, nullable=False)
    image: str = Column(String)
    dt: date = Column(Date)
    clusters: list["Cluster"] = relationship(
        "Cluster", secondary=article_cluster, back_populates="articles", passive_deletes=True, lazy="joined"
    )
