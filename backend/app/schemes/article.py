from datetime import date

from app.schemes.base import CamelModel
from app.schemes.cluster import ClusterORM


class ArticleORM(CamelModel):
    id: int
    url: str
    title: str
    text: str
    image: str
    dt: date
    clusters: list[ClusterORM]

    class Config:
        orm_mode = True
