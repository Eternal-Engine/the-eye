# fmt: off
from enum import Enum

from backend.app.core.settings.app_base_settings import AppBaseSettings, EnvTypes


def test_create_env_types():

    env_types = EnvTypes
    # Test inheritance for EnvTypes from Enum built-in Python class
    assert issubclass(type(Enum), type(env_types))
    assert env_types.PROD.value == "prod"
    assert env_types.DEV.value == "dev"
    assert env_types.TEST.value == "test"
    assert str(env_types.PROD) == "prod"
    assert str(env_types.DEV) == "dev"
    assert str(env_types.TEST) == "test"


def test_get_env_type_name_and_value_by_describe_function():

    env_types = EnvTypes

    assert env_types.PROD.describe() == "PROD: prod"
    assert env_types.DEV.describe() == "DEV: dev"
    assert env_types.TEST.describe() == "TEST: test"


# Test for AppBaseSettings
def test_create_app_base_settings_with_prod_env_as_default_app_env():

    env_types = EnvTypes
    app_base_default_settings = AppBaseSettings()

    assert str(app_base_default_settings) == "Base Settings for App Settings"
    assert isinstance(app_base_default_settings.app_env, env_types)
    assert app_base_default_settings.app_env.describe() == "PROD: prod"


def test_create_app_base_settings_for_dev_env():

    app_base_dev_settings = AppBaseSettings
    app_base_dev_settings.app_env = EnvTypes.DEV

    assert issubclass(EnvTypes, type(app_base_dev_settings().app_env))
    assert app_base_dev_settings.app_env.describe() == "DEV: dev"


def test_create_app_base_settings_for_test_env():

    app_base_test_settings = AppBaseSettings
    app_base_test_settings.app_env = EnvTypes.TEST

    assert issubclass(EnvTypes, type(app_base_test_settings().app_env))
    assert app_base_test_settings.app_env.describe() == "TEST: test"
