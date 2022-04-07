from app.core.settings.app_settings import AppSettings


class AppDevSettings(AppSettings):

    title: str = "iWitness - Backend Development Environment Settings"

    class Config(AppSettings.Config):
        env_file = "env/.env.development"
