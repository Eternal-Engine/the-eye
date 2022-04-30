import decouple

from app.core.settings.app import AppSettings


class AppStagingSettings(AppSettings):
    """
    A class that set up the application with test environment settings.
    """

    title: str = "iWitness - Backend Test Environment Settings"
    database_url: str = decouple.config(
        "DATABASE_TEST_URL",
        cast=str,
    )
    debug: bool = True

    class Config(AppSettings.Config):
        pass
