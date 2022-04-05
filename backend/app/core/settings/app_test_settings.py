import os

from pydantic import SecretStr

from app.core.settings.app_settings import AppSettings


class AppTestSettings(AppSettings):

    title: str = "iWitness - Backend Test Environment Settings"
    debug: bool = SecretStr("DEBUG")
    database_url: str = os.getenv("DATABASE_URL")
    secret_key: SecretStr

    class Config(AppSettings.Config):
        env_file = "env/test_env/test.env"
