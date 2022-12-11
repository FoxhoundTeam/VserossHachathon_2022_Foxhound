from fastapi import APIRouter, Depends

from app import database, schemes
from app.services.auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


@router.get("/me/", response_model=schemes.UserORM, summary="Получить информацию об авторизованном пользователе")
def get_authenticated_user(user: database.User = Depends(get_current_user)):
    return user
