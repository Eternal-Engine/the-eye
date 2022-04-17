import asyncpg
import fastapi
import loguru

from app.core.config import get_settings
from app.core.settings.app import AppSettings
from app.core.settings.base import EnvTypes


async def initialize_db_connection(
    app: fastapi.FastAPI, settings: AppSettings = get_settings(app_env=EnvTypes.DEV)
) -> None:
    """
    A function to initialize database connection with AsyncPG for PostgreSQL.
    """

    loguru.logger.info("Connecting to PostgreSQL database...")

    app.state.pool = await asyncpg.create_pool(
        dsn=str(settings.database_url),
        min_size=settings.min_connection_count,
        max_size=settings.max_connection_count,
    )

    async with app.state.pool.acquire() as con:
        await con.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50),
                    email VARCHAR(50),
                    salt VARCHAR,
                    hashed_password VARCHAR,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                )
            """
        )

    loguru.logger.info("Connection established...")


async def close_db_connection(app: fastapi.FastAPI) -> None:
    """
    A function to shut down database connection.
    """

    loguru.logger.info("Closing connection to database...")

    await app.state.pool.close()

    loguru.logger.info("Connection closed...")
