# fmt: off
from fastapi import FastAPI

from app.main import app


def test_initalize_fastapi_app_in_app():

    my_app = app
    fastapi_app = FastAPI()

    assert isinstance(my_app, type(fastapi_app))
