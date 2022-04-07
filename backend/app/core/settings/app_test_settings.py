import os

from app.core.settings.app_settings import AppSettings


class AppTestSettings(AppSettings):

    title: str = "iWitness - Backend Test Environment Settings"
    database_url: str = os.getenv("DATABASE_URL")  # type: ignore

    class Config(AppSettings.Config):
        env_file = "env/test_env/test.env"
