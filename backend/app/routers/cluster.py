from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from app import schemes
from app.services.auth import get_current_user
from app.services.cluster import ClusterService

router = APIRouter(
    prefix="/clusters",
    tags=["Кластеры"],
)


@router.get("/", response_model=Page[schemes.ClusterORM])
def get_clusters(cluster_service: ClusterService = Depends(), user=Depends(get_current_user)):
    return paginate(cluster_service.all_query())


@router.get("/{id}/", response_model=schemes.ClusterORM)
def get_cluster(id: int, cluster_service: ClusterService = Depends(), user=Depends(get_current_user)):
    return cluster_service.get(id)
