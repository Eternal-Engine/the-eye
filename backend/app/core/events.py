from typing import Any, Coroutine

import fastapi
import loguru

from app.core.settings.app import AppSettings
from app.db.events import close_db_connection, initialize_db_connection


def create_start_app_event_handler(
    app: fastapi.FastAPI,
    settings: AppSettings,
) -> Any:  # type: ignore
    """
    A function that execute all events for the application instance.
    """

    async def start_app_event() -> Coroutine[Any, Any, None]:  # type: ignore

        await initialize_db_connection(app, settings)

    return start_app_event


def create_stop_app_event_handler(app: fastapi.FastAPI) -> Any:  # type: ignore
    """
    A function that shut down all events for the application instance.
    """

    @loguru.logger.catch
    async def stop_app_event() -> Coroutine[Any, Any, None]:  # type: ignore

        await close_db_connection(app)

    return stop_app_event
