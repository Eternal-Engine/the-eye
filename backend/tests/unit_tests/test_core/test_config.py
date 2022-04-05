# fmt: off
from app.core.config import environments, get_settings
from app.core.settings.app_base_settings import EnvTypes
from app.core.settings.app_dev_settings import AppDevSettings
from app.core.settings.app_prod_settings import AppProdSettings
from app.core.settings.app_settings import AppSettings
from app.core.settings.app_test_settings import AppTestSettings


def test_call_settings_from_function_get_settings():

    settings = get_settings()
    app_settings = AppSettings()

    assert settings == app_settings


def test_create_app_environments():

    app_env = environments
    expected = {
        EnvTypes.PROD: AppProdSettings,
        EnvTypes.DEV: AppDevSettings,
        EnvTypes.TEST: AppTestSettings,
    }

    assert isinstance(app_env, dict)
    assert app_env == expected
