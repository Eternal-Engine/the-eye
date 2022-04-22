from typing import AsyncGenerator, Callable, Type

import fastapi
from asyncpg import connection as asyncpg_con, pool as asyncpg_pool

from app.db.repositories.base import BaseRepository


def _get_db_pool(request: fastapi.requests.Request) -> asyncpg_pool.Pool:
    return request.app.state.pool


async def _get_connection_from_pool(
    pool: asyncpg_pool.Pool = fastapi.Depends(_get_db_pool),
) -> AsyncGenerator[asyncpg_con.Connection, None]:
    async with pool.acquire() as conn:
        yield conn


def get_repository(
    repo_type: Type[BaseRepository],
) -> Callable[[asyncpg_con.Connection], BaseRepository]:
    def _get_repo(
        conn: asyncpg_con.Connection = fastapi.Depends(_get_connection_from_pool),
    ) -> BaseRepository:
        return repo_type(conn)

    return _get_repo
