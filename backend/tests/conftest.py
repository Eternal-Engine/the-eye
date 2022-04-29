# fmt: off
# type: ignore

import asgi_lifespan
import fastapi
import httpx
import pytest
from asyncpg import pool as asyncpg_pool

from app.core.config import get_settings
from app.core.settings.base import EnvTypes
from app.db.repositories.journalists import JournalistsRepository
from app.db.repositories.publishers import PublishersRepository
from app.db.repositories.users import UsersRepository
from app.models.domain.journalists import JournalistInDB
from app.models.domain.publishers import PublisherInDB
from app.models.domain.users import UserInDB
from app.services.jwt import generate_access_token
from tests.fake_asyncpg_pool import FakeAsyncPGPool
from tests.tables import create_db_tables, drop_db_tables

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
        await conn.execute(drop_db_tables)

    async with initialized_test_app.state.pool.acquire() as conn:
        await conn.execute(create_db_tables)

    return initialized_test_app.state.pool


@pytest.fixture(name="async_client")
async def async_client(initialized_test_app: fastapi.FastAPI) -> httpx.AsyncClient:

    async with httpx.AsyncClient(
        app=initialized_test_app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:

        yield client


@pytest.fixture(name="authorization_prefix")
def authorization_prefix() -> str:

    settings = get_settings()
    jwt_token_prefix = settings.jwt_token_prefix

    return jwt_token_prefix


@pytest.fixture(name="test_user")
async def test_user(test_pool: asyncpg_pool.Pool) -> UserInDB:
    async with test_pool.acquire() as conn:
        return await UsersRepository(conn).create_user(
            username="usertest",
            email="user.test@test.com",
            password="password-test",
            is_publisher=False,
        )


@pytest.fixture(name="test_user_journalist")
async def test_user_journalist(test_pool: asyncpg_pool.Pool) -> UserInDB:
    async with test_pool.acquire() as conn:
        return await UsersRepository(conn).create_user(
            username="usertest2",
            email="user2.test2@test.com",
            password="password2-test2",
            is_publisher=False,
        )


@pytest.fixture(name="test_user_publisher")
async def test_user_publisher(test_pool: asyncpg_pool.Pool) -> UserInDB:
    async with test_pool.acquire() as conn:
        return await UsersRepository(conn).create_user(
            username="usertest3",
            email="user3.test3@test.com",
            password="password3-test3",
            is_publisher=True,
        )


@pytest.fixture(name="test_user_publisher_2")
async def test_user_publisher_2(test_pool: asyncpg_pool.Pool) -> UserInDB:
    async with test_pool.acquire() as conn:
        return await UsersRepository(conn).create_user(
            username="usertest4",
            email="user4.test4@test.com",
            password="password4-test4",
            is_publisher=True,
        )


@pytest.fixture(name="test_journalist")
async def test_journalist(
    test_user: UserInDB,
    test_pool: asyncpg_pool.Pool) -> JournalistInDB:
    async with test_pool.acquire() as conn:
        return await JournalistsRepository(conn).create_journalist_by_username(
            username=test_user.username,
            first_name="Tester",
            last_name="Journalist",
            profile_picture="home/test/pp/journalist.png",
            banner="home/test/banner/journalist_banner.png",
            bio="Awesome super journalist",
            address="Secretstreet 666",
            postal_code="13055",
            state="Kuta",
            country="Dreamland",
            office_phone_number="+666",
            mobile_phone_number="+666911",
        )


@pytest.fixture(name="test_publisher")
async def test_publisher(
    test_user_publisher: UserInDB,
    test_pool: asyncpg_pool.Pool) -> PublisherInDB:
    async with test_pool.acquire() as conn:
        return await PublishersRepository(conn).create_publisher_by_username(
            username=test_user_publisher.username,
            name="AxelSpringer",
            profile_picture="home/test/pp/AxelSpringer.png",
            banner="home/test/banner/AxelSPringerBanner.png",
            bio="Biggest media house in Europe!",
            address="Zimmermannstr. 50",
            postal_code="14350",
            state="Mitte",
            country="Germany",
            office_phone_number="+6661234567",
            mobile_phone_number="+66691112314",
        )


@pytest.fixture(name="test_token")
def test_token(test_user: UserInDB) -> str:
    return generate_access_token(test_user)


@pytest.fixture(name="authorized_async_client")
def authorized_async_client(
    async_client: httpx.AsyncClient,
    test_token: str,
    authorization_prefix: str) -> httpx.AsyncClient:

    async_client.headers = {
        "Authorization": f"{authorization_prefix} {test_token}",
        **async_client.headers,
    }

    return async_client
