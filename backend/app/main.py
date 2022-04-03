from fastapi import FastAPI

from app.core.config import get_settings

settings = get_settings()
app = FastAPI(**settings.fastapi_kwargs)


@app.get("/app_settings", tags=["App Settings"])
async def get_app_settings():

    return {
        "environment": settings.ENV,
        "database_url": settings.database_url,
    }
