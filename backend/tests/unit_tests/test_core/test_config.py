# fmt: off
from app.core.config import environments, get_settings
from app.core.settings.base import EnvTypes
from app.core.settings.development import AppDevSettings
from app.core.settings.production import AppProdSettings
from app.core.settings.staging import AppStagingSettings


def test_call_default_settings_from_function_get_settings():

    default_settings = get_settings()
    app_prod_settings = AppProdSettings()

    assert default_settings == app_prod_settings


def test_create_app_environments():

    app_env = environments
    expected = {
        EnvTypes.PROD: AppProdSettings,
        EnvTypes.DEV: AppDevSettings,
        EnvTypes.TEST: AppStagingSettings,
    }

    assert isinstance(app_env, dict)
    assert app_env == expected


def test_call_dev_app_settings_from_function_get_settings():

    dev_settings = get_settings(EnvTypes.DEV)
    app_dev_settings = AppDevSettings()

    assert dev_settings == app_dev_settings


def test_call_test_app_settings_from_function_get_settings():

    test_settings = get_settings(EnvTypes.TEST)
    app_test_settings = AppStagingSettings()

    assert test_settings == app_test_settings
