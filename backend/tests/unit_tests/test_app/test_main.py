# fmt: off
import fastapi

import app
from app.main import app as my_app


def test_app_version() -> None:

    assert app.__version__ == "0.1.0"


def test_application_is_fastapi_instance() -> None:

    app = my_app
    fastapi_app = fastapi.FastAPI

    assert isinstance(app, fastapi_app)
    assert app.redoc_url == "/redoc"
    assert app.docs_url == "/docs"
    assert app.openapi_url == "/openapi.json"
    assert app.redoc_url == "/redoc"
