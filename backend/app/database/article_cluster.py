from sqlalchemy import Column, ForeignKey, Integer, Table

from app.database.base import Base

article_cluster = Table(
    "article_cluster",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("article.id"), primary_key=True),
    Column("cluster_id", Integer, ForeignKey("cluster.id"), primary_key=True),
)
