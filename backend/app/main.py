import fastapi
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router as api_router
from app.api.errors.events import http422_error_handler, http_error_handler
from app.core.config import get_settings
from app.core.events import create_start_app_event_handler, create_stop_app_event_handler
from app.core.settings.app import AppSettings
from app.core.settings.base import EnvTypes


def initialize_application(settings: AppSettings = get_settings(EnvTypes.DEV)) -> fastapi.FastAPI:
    """
    A function to initialize FastAPI instance with a customized application settings, database connection,
    and API endpoints for the backend application.
    """

    # FastAPI instance initialized with AppSettings attributes
    application = fastapi.FastAPI(**settings.fastapi_kwargs)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Connect and disconnect database event handlers
    application.add_event_handler(
        "startup",
        create_start_app_event_handler(application, settings),
    )
    application.add_event_handler(
        "shutdown",
        create_stop_app_event_handler(application),
    )

    application.add_exception_handler(fastapi.HTTPException, http_error_handler)
    application.add_exception_handler(fastapi.exceptions.RequestValidationError, http422_error_handler)

    # Append all routes to endpoints
    application.include_router(api_router, prefix=settings.api_prefix)

    return application


app = initialize_application()
