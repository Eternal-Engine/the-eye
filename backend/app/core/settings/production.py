from app.core.settings.app import AppSettings


class AppProdSettings(AppSettings):
    """
    A class that set up the application with production environment settings.
    """

    class Config(AppSettings.Config):
        pass
