from app.core.settings.app_settings import AppSettings


class AppProdSettings(AppSettings):
    class Config(AppSettings.Config):
        env_file = "env/prod_env/prod.env"
