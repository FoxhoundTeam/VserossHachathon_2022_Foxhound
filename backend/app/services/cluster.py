from sqlalchemy import func

from app.database import Cluster
from app.database.article_cluster import article_cluster
from app.services.base import BaseDBService
from app.utils import get_or_404


class ClusterService(BaseDBService):
    def all_query(self):
        s = (
            self.session.query(article_cluster.c.cluster_id, func.count("*").label("articles_count"))
            .group_by(article_cluster.c.cluster_id)
            .subquery()
        )
        return (
            self.session.query(
                Cluster.id,
                Cluster.theme,
                Cluster.lon,
                Cluster.lat,
                Cluster.class_name,
                Cluster.location,
                func.coalesce(s.c.articles_count, 0).label("articles_count"),
            )
            .outerjoin(s, Cluster.id == s.c.cluster_id)
            .order_by(Cluster.id)
        )

    def get(self, id_: int) -> Cluster:
        return get_or_404(self.session, Cluster, id_, "Кластер не найден")
