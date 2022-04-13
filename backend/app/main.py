from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router as api_router
from app.core.config import get_settings
from app.core.events import create_start_app_handler, create_stop_app_handler
from app.core.settings.app_base_settings import EnvTypes
from app.core.settings.app_settings import AppSettings
from app.db.database import engine, metadata


def initialize_application(settings: AppSettings = get_settings(EnvTypes.DEV)) -> FastAPI:

    # metadata.drop_all(engine)
    metadata.create_all(engine)

    application = FastAPI(**settings.fastapi_kwargs)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Event (database) handler
    application.add_event_handler("startup", create_start_app_handler())

    application.add_event_handler("shutdown", create_stop_app_handler())

    # Add all routes
    application.include_router(api_router, prefix=settings.api_prefix)

    return application


app = initialize_application()
