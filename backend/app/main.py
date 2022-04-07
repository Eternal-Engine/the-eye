from fastapi import FastAPI

from app.core.config import get_settings, log
from app.core.settings.app_base_settings import EnvTypes
from app.db.database import init_db

settings = get_settings(app_env=EnvTypes.DEV)
app = FastAPI(**settings.fastapi_kwargs)


@app.on_event("startup")
async def startup():
    await init_db()
    log.info("Database setup is DONE...")


@app.get("/app_settings", tags=["App Settings"])
async def get_app_settings():

    return {
        "environment": settings.app_env,
    }
