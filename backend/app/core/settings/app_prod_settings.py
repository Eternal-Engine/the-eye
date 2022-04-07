from backend.app.core.settings.app_settings import AppSettings


class AppProdSettings(AppSettings):
    class Config(AppSettings.Config):
        pass
