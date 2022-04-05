from pydantic import SecretStr

from app.core.settings.app_settings import AppSettings


class AppTestSettings(AppSettings):

    title: str = "iWitness - Backend Test Environment Settings"
    database_url: str = SecretStr("DATABASE_URL")

    class Config(AppSettings.Config):
        env_file = "env/test_env/test.env"
