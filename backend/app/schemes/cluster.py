from app.schemes.base import CamelModel


class ClusterORM(CamelModel):
    id: int
    theme: list[str]
    class_name: str
    location: str
    lat: float
    lon: float

    class Config:
        orm_mode = True
