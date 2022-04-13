from fastapi import APIRouter

from app.api.routes import app_settings, users

router = APIRouter()
router.include_router(app_settings.router)
router.include_router(users.router)
