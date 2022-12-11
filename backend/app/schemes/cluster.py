from app.schemes.base import CamelModel


class ClusterORM(CamelModel):
    id: int
    theme: list[str]
    class_name: str
    location: str
    lat: float
    lon: float
    articles_count: int = 0

    class Config:
        orm_mode = True
