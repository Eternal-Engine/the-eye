from fastapi import APIRouter

from app.api.routes import authentication as auth

router = APIRouter()
router.include_router(auth.router)
