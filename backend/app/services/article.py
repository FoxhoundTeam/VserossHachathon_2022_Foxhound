from app.database import Article
from app.services.base import BaseDBService
from app.utils import get_or_404


class ArticleService(BaseDBService):
    def all_query(self):
        return self.session.query(Article)

    def get(self, id_: int) -> Article:
        return get_or_404(self.session, Article, id_, "Статья не найдена")
