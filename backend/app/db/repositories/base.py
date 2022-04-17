from asyncpg import connection as asyncpg_con


class BaseRepository:
    def __init__(self, conn: asyncpg_con.Connection) -> None:
        self._conn = conn

    @property
    def connection(self) -> asyncpg_con.Connection:
        return self._conn
