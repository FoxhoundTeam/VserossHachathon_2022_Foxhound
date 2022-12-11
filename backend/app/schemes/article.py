from datetime import date

from app.schemes.base import CamelModel


class ArticleORM(CamelModel):
    id: int
    url: str
    title: str
    text: str
    image: str
    dt: date

    class Config:
        orm_mode = True
