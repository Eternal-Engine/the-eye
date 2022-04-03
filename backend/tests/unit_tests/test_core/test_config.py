from pydantic import BaseSettings

from app.core.config import Settings


def test_settings_construction():

    pydantic_base_settings = BaseSettings
    settings = Settings

    assert issubclass(settings, pydantic_base_settings)
    assert settings().__str__() == "Application Settings"
    assert settings().ENV == "dev"
    assert settings().TESTING == 1
