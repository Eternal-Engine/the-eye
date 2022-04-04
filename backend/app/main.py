from fastapi import FastAPI

from app.core.config import get_settings
from app.db.database import Base, engine

settings = get_settings()
app = FastAPI(**settings.fastapi_kwargs)


@app.on_event("startup")
async def startup():
    # create db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.get("/app_settings", tags=["App Settings"])
async def get_app_settings():

    return {
        "environment": settings.app_env,
        "database_url": settings.database_url,
    }
