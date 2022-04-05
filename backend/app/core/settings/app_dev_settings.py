from pydantic import PostgresDsn, SecretStr

from app.core.settings.app_settings import AppSettings


class AppDevSettings(AppSettings):

    title: str = "iWitness - Backend Development Environment Settings"
    debug: bool = SecretStr("DEBUG")
    database_url: PostgresDsn
    secret_key: SecretStr

    class Config(AppSettings.Config):
        env_file = "env/dev_env/dev.env"
