import asyncpg
from fastapi import FastAPI
from loguru import logger

from app.core.settings.app_settings import AppSettings


async def initialize_db_connection(app: FastAPI, settings: AppSettings) -> None:
    """
    A function to initialize database connection with AsyncPG for PostgreSQL.
    """

    logger.info("Connecting to PostgreSQL database...")

    app.state.pool = await asyncpg.create_pool(
        str(settings.database_url),
        min_size=settings.min_connection_count,
        max_size=settings.max_connection_count,
    )

    logger.info("Connection established...")


async def close_db_connection(app: FastAPI) -> None:
    """
    A function to shut down database connection.
    """

    logger.info("Closing connection to database...")

    await app.state.pool.close()

    logger.info("Connection closed...")
