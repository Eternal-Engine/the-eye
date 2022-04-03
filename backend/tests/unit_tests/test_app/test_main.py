import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.main import app


def test_initalize_fastapi_app_in_app():

    my_app = app
    fastapi_app = FastAPI()

    assert isinstance(my_app, type(fastapi_app))


# Async test is not yet provided by unittest, hence using pytest
@pytest.mark.anyio
async def test_app_settings_route_response_200():

    expected = {"environment": "dev", "database_url": "sqlite:///iW_dev.sqlite3"}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/app_settings")

    assert response.status_code == 200
    assert response.json() == expected
