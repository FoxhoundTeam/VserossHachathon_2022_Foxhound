from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from app import schemes
from app.services.article import ArticleService
from app.services.auth import get_current_user

router = APIRouter(
    prefix="/articles",
    tags=["Статьи"],
)


@router.get("/", response_model=Page[schemes.ArticleORM])
def get_articles(article_service: ArticleService = Depends(), user=Depends(get_current_user)):
    return paginate(article_service.all_query())


@router.get("/{id}/", response_model=schemes.ArticleORM)
def get_article(id: int, article_service: ArticleService = Depends(), user=Depends(get_current_user)):
    return article_service.get(id)
