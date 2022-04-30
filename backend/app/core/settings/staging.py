from app.core.settings.app import AppSettings


class AppStagingSettings(AppSettings):
    """
    A class that set up the application with test environment settings.
    """

    title: str = "iWitness - Backend Test Environment Settings"
    database_url: str = "postgresql://postgres:postgres@0.0.0.0:5432/iW_test"
    debug: bool = True

    class Config(AppSettings.Config):
        pass
