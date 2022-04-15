# fmt: off
from fastapi import FastAPI

import app as app_module
from app.main import app


def test_app_version():

    assert app_module.__version__ == "0.1.0"


def test_application_is_fastapi_instance():

    my_app = app
    fastapi_app = FastAPI

    assert isinstance(my_app, fastapi_app)
    assert my_app.redoc_url == "/redoc"
    assert my_app.docs_url == "/docs"
    assert my_app.openapi_url == "/openapi.json"
    assert my_app.redoc_url == "/redoc"
