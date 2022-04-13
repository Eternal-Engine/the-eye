from typing import Any, Callable

from app.db.events import shutdown_app_db_connection, startup_app_db_connection


def create_start_app_handler() -> Callable:
    async def start_app() -> Any:

        return await startup_app_db_connection()

    return start_app


def create_stop_app_handler() -> Callable:
    async def stop_app() -> Any:
        return await shutdown_app_db_connection()

    return stop_app
