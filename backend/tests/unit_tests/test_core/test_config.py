from pydantic import BaseSettings

from app.core.config import Settings, get_settings


def test_settings_construction():

    pydantic_base_settings = BaseSettings
    settings = Settings

    assert issubclass(settings, pydantic_base_settings)
    assert settings().__str__() == "Application Settings"
    assert settings().ENV == "dev"
    assert settings().TESTING == 1


def test_get_settings_function_to_get_application_settings():

    settings = Settings
    settings_from_get_settings = get_settings()

    assert isinstance(settings_from_get_settings, settings)
