import pathlib

import aiosql

queries = aiosql.from_path(sql_path=pathlib.Path(__file__).parent / "sql", driver_adapter="asyncpg")
