from typing import Any, Callable

from app.db.events import shutdown_app_db_connection, startup_app_db_connection


def create_start_app_handler() -> Callable:
    """
    A function that handles the general event starter.
    """

    async def start_app_events() -> Any:

        return await startup_app_db_connection()

    return start_app_events


def create_stop_app_handler() -> Callable:
    """
    A function that handles the stopage of general events.
    """

    async def stop_app_events() -> Any:

        return await shutdown_app_db_connection()

    return stop_app_events
