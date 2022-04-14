# fmt: off
# type: ignore

import pytest
from fastapi import FastAPI

from app.core.config import get_settings
from app.core.settings.app_base_settings import EnvTypes

# Set up the `app_env` to use the TEST environment settings
settings = get_settings(app_env=EnvTypes.TEST)


@pytest.fixture(name="test_app")
def test_app() -> FastAPI:
    """
    A fixture that re-initializes the FastAPI instance for test application.
    """

    from app.main import initialize_application  # local import for testing purpose

    return initialize_application(settings=settings)
