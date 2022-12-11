from app.database import Cluster
from app.services.base import BaseDBService
from app.utils import get_or_404


class ClusterService(BaseDBService):
    def all_query(self):
        return self.session.query(Cluster)

    def get(self, id_: int) -> Cluster:
        return get_or_404(self.session, Cluster, id_, "Кластер не найден")
