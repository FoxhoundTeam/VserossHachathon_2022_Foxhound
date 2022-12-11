from sqlalchemy import Column, String

from app.database.base import Base


class User(Base):
    """Пользователь."""

    email: str = Column(String, unique=True, nullable=False)
    password_hash: str = Column(String, nullable=False)
