from pydantic import EmailStr

from app.schemes.base import CamelModel


class BaseUser(CamelModel):
    email: EmailStr


class UserCreate(BaseUser):
    password: str


class UserVerifyToken(BaseUser):
    id: int


class UserORM(UserVerifyToken):
    class Config:
        orm_mode = True
