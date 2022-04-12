from fastapi import APIRouter, status

from app.core.config import get_settings

router = APIRouter(
    tags=["App Settings"],
)


@router.get("/app_settings/", status_code=status.HTTP_200_OK)
async def get_app_settings():
    settings = get_settings()

    return {
        "environment": settings.app_env,
    }
