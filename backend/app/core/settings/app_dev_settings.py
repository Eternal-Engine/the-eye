from app.core.settings.app_settings import AppSettings


class AppDevSettings(AppSettings):

    title: str = "iWitness - Backend Development Environment Settings"
    debug: bool = True

    class Config(AppSettings.Config):
        env_file = "env/.env.development"
