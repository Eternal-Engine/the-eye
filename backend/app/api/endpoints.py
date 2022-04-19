from fastapi import APIRouter

from app.api.routes.authentication import router as auth_router

router = APIRouter()
router.include_router(auth_router)
