from fastapi import APIRouter

from app.api.routes.authentication import router as auth_router
from app.api.routes.users import router as users_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(users_router)
