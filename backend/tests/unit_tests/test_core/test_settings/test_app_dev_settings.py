from pydantic import PostgresDsn

from app.core.settings.app_base_settings import EnvTypes
from app.core.settings.app_dev_settings import AppDevSettings


def test_create_app_prod_settings():

    app_dev_settings = AppDevSettings()

    expected = {
        "app_env": EnvTypes.DEV,
        "title": "iWitness - Backend Development Environment Settings",
        "description": "A backend project with FastAPI for iWitness web application.",
        "version": "0.0.0",
        "debug": True,
        "database_url": PostgresDsn(
            "postgresql+asyncpg://postgres:postgres@localhost:5432/iW_dev",
            scheme="postgresql+asyncpg",
            user="postgres",
            password="postgres",
            host="localhost",
            host_type="int_domain",
            port="5432",
            path="/iW_dev",
        ),
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "openapi_url": "/openapi.json",
        "api_prefix": "/api",
        "openapi_prefix": "",
        "jwt_token_prefix": "Token",
        "allowed_hosts": ["*"],
    }

    assert app_dev_settings.dict(exclude={"secret_key"}) == expected
    assert app_dev_settings.Config.env_file == "env/dev_env/dev.env"
    assert app_dev_settings.Config.validate_assignment is True
