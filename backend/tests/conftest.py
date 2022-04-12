# fmt: off
import databases
import pytest
import sqlalchemy
from starlette.testclient import TestClient

from app.core.config import get_settings
from app.core.settings.app_base_settings import EnvTypes
from app.main import app

# Set up the `app_env` to use the TEST environment settings
settings = get_settings(app_env=EnvTypes.TEST)
TEST_DATABASE_URL = settings.database_url

# Databases query builder
test_database = databases.Database(TEST_DATABASE_URL, force_rollback=True)

test_engine = sqlalchemy.create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
metadata = sqlalchemy.MetaData()


@pytest.fixture(name="async_client")
@pytest.mark.anyio  # Using asynchronous backend from AsyncIO
async def async_client():

    # Drop all tables from the previous test session
    metadata.drop_all(test_engine)

    # Create all DB tables for the current test session
    metadata.create_all(test_engine)

    # Connect to test_database: sqlite:///.iW_test.sqlite3
    await test_database.connect()

    # Initialize the test client for endpoint request
    client = TestClient(app)
    yield client  # The testing start here!

    # Disconnect from the database after all test is done!
    await test_database.disconnect()
