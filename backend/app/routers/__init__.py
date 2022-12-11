from fastapi import APIRouter

from . import article, auth, cluster, scan, user

router = APIRouter(prefix="/api")
router.include_router(auth.router)
router.include_router(user.router)
router.include_router(article.router)
router.include_router(cluster.router)
router.include_router(scan.router)
