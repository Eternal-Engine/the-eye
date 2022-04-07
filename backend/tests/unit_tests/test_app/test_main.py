# fmt: off
import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.main import app, settings


def test_initalize_fastapi_app_in_app():

    my_app = app
    fastapi_app = FastAPI()

    assert isinstance(my_app, type(fastapi_app))


# Async test is not yet provided by unittest, hence using pytest
@pytest.mark.anyio
async def test_async_app_settings_route_response_200():

    expected = {"environment": "prod", "database_url": settings.database_url}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/app_settings")

    assert response.status_code == 200
    assert response.json() == expected
