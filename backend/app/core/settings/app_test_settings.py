from app.core.settings.app_settings import AppSettings


class AppTestSettings(AppSettings):

    title: str = "iWitness - Backend Test Environment Settings"

    class Config(AppSettings.Config):
        env_file = "env/.env.test"
