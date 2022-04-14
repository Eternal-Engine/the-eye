# fmt: off
# type: ignore
import databases
import pytest
import sqlalchemy
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.testclient import TestClient

from app.core.config import get_settings
from app.core.settings.app_base_settings import EnvTypes

# Set up the `app_env` to use the TEST environment settings
settings = get_settings(app_env=EnvTypes.TEST)
TEST_DATABASE_URL = settings.database_url

# Databases query builder
test_database = databases.Database(TEST_DATABASE_URL, force_rollback=True)

metadata = sqlalchemy.MetaData()


@pytest.fixture(name="test_app")
def test_app() -> FastAPI:
    from app.main import initialize_application  # type: ignore

    return initialize_application(settings=settings)


def create_and_drop_test_database():

    # Create test database and DB tables
    test_engine = sqlalchemy.create_engine(
        TEST_DATABASE_URL, connect_args={"check_same_thread": False}, future=True, echo=True
    )
    metadata.create_all(test_engine)

    # Run the test suite
    yield

    # Delete all DB tables
    metadata.drop_all(test_engine)


@pytest.fixture(name="async_client")
async def async_client(test_app: FastAPI) -> AsyncClient:

    create_and_drop_test_database()

    # Initialize the test client for endpoint request
    with TestClient(test_app) as client:

        yield client  # The testing start here!
