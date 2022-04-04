# fmt: off
from app.core.config import get_settings
from app.core.settings.app_settings import AppSettings


def test_call_settings_from_function_get_settings():

    settings = get_settings()
    app_settings = AppSettings

    assert isinstance(settings, app_settings)
