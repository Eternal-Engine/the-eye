from fastapi import FastAPI

from app.core.config import get_settings

settings = get_settings()
app = FastAPI()


async def get_app_settings():
    pass
