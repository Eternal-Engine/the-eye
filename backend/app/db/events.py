# type: ignore
from typing import Any, Coroutine

from app.db.database import database


async def startup_app_db_connection() -> Coroutine[Any, Any, None]:

    try:
        await database.connect()
    except ConnectionError:
        print("Connection to the database cannot be established...")


async def shutdown_app_db_connection() -> Coroutine[Any, Any, None]:

    try:
        await database.disconnect()
    except ConnectionError:
        print("Connection to the database cannot be established...")
