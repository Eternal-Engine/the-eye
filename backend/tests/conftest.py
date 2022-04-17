# fmt: off
# type: ignore

import asgi_lifespan
import fastapi
import httpx
import pytest
from asyncpg import pool as asyncpg_pool

from app.core.config import get_settings
from app.core.settings.base import EnvTypes
from app.db.queries import database
from tests.fake_asyncpg_pool import FakeAsyncPGPool

# Set up the "app_env" to use the TEST environment settings
test_settings = get_settings(app_env=EnvTypes.TEST)


@pytest.fixture(name="test_app")
def test_app() -> fastapi.FastAPI:
    """
    A fixture that re-initializes the FastAPI instance for test application.
    """

    from app.main import initialize_application  # local import for testing purpose

    return initialize_application(settings=test_settings)


@pytest.fixture(name="initialized_test_app")
async def initialized_test_app(test_app: fastapi.FastAPI) -> fastapi.FastAPI:

    async with asgi_lifespan.LifespanManager(test_app):

        test_app.state.pool = await FakeAsyncPGPool.create_pool(test_app.state.pool)
        yield test_app


@pytest.fixture(scope="function", name="test_pool")
async def test_pool(initialized_test_app: fastapi.FastAPI) -> asyncpg_pool.Pool:

    async with initialized_test_app.state.pool.acquire() as conn:
        await conn.execute(database.drop_db_tables)

    async with initialized_test_app.state.pool.acquire() as conn:
        await conn.execute(database.create_db_tables)

    return initialized_test_app.state.pool


@pytest.fixture(name="async_client")
async def async_client(initialized_test_app: fastapi.FastAPI) -> httpx.AsyncClient:

    async with httpx.AsyncClient(
        app=initialized_test_app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:

        yield client


# @pytest.fixture
# async def test_user(pool: asyncpg_pool.Pool) -> users_domain.UserInDB:
#     async with pool.acquire() as conn:
#         return await users_repo.UsersRepository(conn).create_user(
#             email="user_test@test.com", password="password-test", username="usertest",
#         )

# @pytest.fixture(name="auth_jwt_prefix")
# def auth_jwt_prefix() -> str:

#     return settings.jwt_token_prefix


# @pytest.fixture(name="token")
# def token(test_user: users_domain.UserInDB) -> str:
#     return jwt_services.create_access_token(test_user, jwt_services.SECRET_KEY_JWT)
