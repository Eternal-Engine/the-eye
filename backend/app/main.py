from fastapi import FastAPI

from app.api.routes.app_settings import router as app_settings_routes
from app.api.routes.users import router as user_routes
from app.core.config import get_settings, log
from app.core.settings.app_base_settings import EnvTypes
from app.db.database import database, engine, metadata

# metadata.drop_all(engine)
metadata.create_all(engine)

settings = get_settings(app_env=EnvTypes.DEV)
app = FastAPI(**settings.fastapi_kwargs)
app.include_router(user_routes)
app.include_router(app_settings_routes)


@app.on_event("startup")
async def startup():
    await database.connect()
    log.info("Database is successfully CONNECTED...")


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    log.info("Database is DISCONNECTED...")
