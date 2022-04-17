import decouple

from app.core.settings.app import AppSettings


class AppDevSettings(AppSettings):
    """
    A class that set up the application with devlopment environment settings.
    """

    title: str = "iWitness - Backend Development Environment Settings"
    debug: bool = decouple.config("DEV_DEBUG", cast=bool)
    database_url: str = decouple.config("DEV_DATABASE_URL", cast=str)
    secret_key: str = decouple.config("DEV_SECRET_KEY", cast=str)

    class Config(AppSettings.Config):
        pass
