from pydantic import PostgresDsn, SecretStr

from app.core.settings.app_settings import AppSettings


class AppProdSettings(AppSettings):

    database_url: PostgresDsn
    secret_key: SecretStr

    class Config(AppSettings.Config):
        env_file = "env/prod_env/prod.env"
