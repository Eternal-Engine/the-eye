# type: ignore
from typing import Any, Coroutine

from app.core.logging import log

# type: ignore
from app.db.database import DATABASE_URL, database, engine, metadata


def create_db_tables():
    """
    A function to create all DB tables.
    """

    # metadata.drop_all(engine)
    metadata.create_all(engine)


async def startup_app_db_connection() -> Coroutine[Any, Any, None]:
    """
    A function to create a connection to the database.
    """

    try:
        log.info("Starting connection to database...")
        log.info(f"Database URL: {DATABASE_URL}")

        await database.connect()

        log.info("Connection to database is successfully established...")

    except (ConnectionError, ConnectionRefusedError):

        log.info("Fail to connect with the database!!!")


async def shutdown_app_db_connection() -> Coroutine[Any, Any, None]:
    """
    A function to shutdown the connection to the database.
    """

    try:
        await database.disconnect()
        log.info("Database is successfully disconnected...")

    except ConnectionError:

        log.info("Fail to connect with the database!!!")
