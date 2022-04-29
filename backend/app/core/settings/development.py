from app.core.settings.app import AppSettings


class AppDevSettings(AppSettings):
    """
    A class that set up the application with devlopment environment settings.
    """

    title: str = "iWitness - Backend Development Environment Settings"
    debug: bool = True

    class Config(AppSettings.Config):
        pass
