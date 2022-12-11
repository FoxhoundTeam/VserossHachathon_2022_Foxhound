from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from app import schemes
from app.services.auth import get_current_user
from app.services.scan_service import ScanService

router = APIRouter(
    prefix="/scans",
    tags=["Сканы"],
)


@router.post("/", response_model=schemes.ScanORM)
def start_scan(scan_data: schemes.ScanCreate, scan_service: ScanService = Depends(), user=Depends(get_current_user)):
    return scan_service.start_scan(scan_data.ip)


@router.get("/", response_model=Page[schemes.ScanORM])
def get_scans(scan_service: ScanService = Depends(), user=Depends(get_current_user)):
    return paginate(scan_service.all_query())


@router.get("/{id}/", response_model=schemes.ScanORM)
def get_scan(id: int, scan_service: ScanService = Depends(), user=Depends(get_current_user)):
    return scan_service.get(id)


@router.get("/{id}/services/", response_model=list[schemes.ServiceORM])
def get_scan_services(id: int, scan_service: ScanService = Depends(), user=Depends(get_current_user)):
    return scan_service.get(id).services
