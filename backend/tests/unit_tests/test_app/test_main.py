from fastapi import FastAPI

from app.main import app


def test_initalize_fastapi_app_in_app():

    my_app = app
    fastapi_app = FastAPI()

    assert isinstance(my_app, type(fastapi_app))


async def test_async_app_settings_route_response_200(async_client):

    expected = {"environment": "prod"}

    response = async_client.get("/app_settings/")

    assert response.status_code == 200
    assert response.json() == expected
