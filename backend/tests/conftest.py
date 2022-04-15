# fmt: off
# type: ignore


import pytest
from asgi_lifespan import LifespanManager
from asyncpg.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient

from app.core.config import get_settings
from app.core.settings.app_base_settings import EnvTypes
from tests.fake_asyncpg_pool import FakeAsyncPGPool

# Set up the `app_env` to use the TEST environment settings
settings = get_settings(app_env=EnvTypes.TEST)


@pytest.fixture(name="test_app")
def test_app() -> FastAPI:
    """
    A fixture that re-initializes the FastAPI instance for test application.
    """

    from app.main import initialize_application  # local import for testing purpose

    return initialize_application(settings=settings)


@pytest.fixture(name="initialized_test_app")
async def initialized_test_app(test_app: FastAPI) -> FastAPI:
    async with LifespanManager(test_app):
        test_app.state.pool = await FakeAsyncPGPool.create_pool(test_app.state.pool)
        yield test_app


@pytest.fixture(name="pool")
def pool(initialized_test_app: FastAPI) -> Pool:
    return initialized_test_app.state.pool


@pytest.fixture(name="async_client")
async def async_client(initialized_test_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=initialized_test_app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client
