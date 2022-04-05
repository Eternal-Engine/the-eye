# fmt: off
from app.core.config import app_environments, get_settings
from app.core.settings.app_settings import AppSettings


def test_call_settings_from_function_get_settings():

    settings = get_settings()
    app_settings = AppSettings

    assert isinstance(settings, app_settings)


def test_create_app_environments():

    app_env = app_environments

    assert isinstance(app_env, dict)
