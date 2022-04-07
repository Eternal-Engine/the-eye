from app.core.settings.app_settings import AppSettings


class AppTestSettings(AppSettings):

    title: str = "iWitness - Backend Test Environment Settings"
    debug: bool = True

    class Config(AppSettings.Config):
        env_file = "env/.env.test"
