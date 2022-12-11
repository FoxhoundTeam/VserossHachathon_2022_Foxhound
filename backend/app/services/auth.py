from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jose import JWTError, jwt
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import database, schemes
from app.config import settings
from app.services.base import BaseDBService

JWTHeader = APIKeyHeader(name="Authorization")


def get_current_user(
    token: str = Depends(JWTHeader), session: Session = Depends(database.get_session)
) -> database.User:
    user: database.User = (
        session.query(database.User).filter(database.User.id == AuthService.verify_token(token).id).first()
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    return user


class AuthService(BaseDBService):
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def verify_token(cls, token: str) -> schemes.UserVerifyToken:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise exception from None

        user_data = payload.get("user")

        try:
            user = schemes.UserVerifyToken.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def create_token(cls, user: database.User) -> schemes.Token:
        user_data = schemes.UserORM.from_orm(user)
        now = datetime.utcnow()
        payload = {
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(seconds=settings.jwt_expires_s),
            "sub": str(user_data.id),
            "user": user_data.dict(include={"id", "email"}),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        return schemes.Token(access_token=token)

    def register_new_user(self, user_data: schemes.UserCreate) -> schemes.Token:
        if self.session.query(database.User).filter(database.User.email == user_data.email).first() is not None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="This email already exist",
            )
        user = database.User(
            password_hash=self.hash_password(user_data.password), **user_data.dict(exclude={"password"})
        )
        self._save_obj(user)

        return self.create_token(user)

    def authenticate_user(self, email: str, password: str) -> schemes.Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

        user: Optional[database.User] = self.session.query(database.User).filter(database.User.email == email).first()

        if not user or not user.is_active:
            raise exception

        if not self.verify_password(password, user.password_hash):
            raise exception

        return self.create_token(user)

    def change_password(self, data: schemes.ChangePassword, user: database.User):
        user.password_hash = self.hash_password(data.password)
        self._save_obj(user)
