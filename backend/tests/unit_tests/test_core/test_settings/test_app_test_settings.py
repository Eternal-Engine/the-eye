from pydantic import PostgresDsn

from app.core.settings.app_base_settings import EnvTypes
from app.core.settings.app_test_settings import AppTestSettings


def test_create_app_prod_settings():

    app_test_settings = AppTestSettings()

    expected = {
        "app_env": EnvTypes.TEST,
        "title": "iWitness - Backend Test Environment Settings",
        "description": "A backend project with FastAPI for iWitness web application.",
        "version": "0.0.0",
        "debug": True,
        "database_url": PostgresDsn(
            "postgresql+asyncpg://postgres:postgres@localhost:5432/iW_test",
            scheme="postgresql+asyncpg",
            user="postgres",
            password="postgres",
            host="localhost",
            host_type="int_domain",
            port="5432",
            path="/iW_test",
        ),
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "openapi_url": "/openapi.json",
        "api_prefix": "/api",
        "openapi_prefix": "",
        "jwt_token_prefix": "Token",
        "allowed_hosts": ["*"],
    }

    assert app_test_settings.dict(exclude={"secret_key"}) == expected
    assert app_test_settings.Config.env_file == "env/test_env/test.env"
    assert app_test_settings.Config.validate_assignment is True
