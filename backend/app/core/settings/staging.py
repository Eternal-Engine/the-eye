import decouple

from app.core.settings.app import AppSettings


class AppStagingSettings(AppSettings):
    """
    A class that set up the application with test environment settings.
    """

    title: str = "iWitness - Backend Test Environment Settings"
    debug: bool = decouple.config("TEST_DEBUG", cast=bool)
    database_url: str = decouple.config("TEST_DATABASE_URL", cast=str)
    secret_key: str = decouple.config("TEST_SECRET_KEY", cast=str)

    class Config(AppSettings.Config):
        pass
