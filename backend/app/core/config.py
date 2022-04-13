from functools import lru_cache
from typing import Dict, Type

from app.core.logging import log
from app.core.settings.app_base_settings import AppBaseSettings, EnvTypes
from app.core.settings.app_dev_settings import AppDevSettings
from app.core.settings.app_prod_settings import AppProdSettings
from app.core.settings.app_settings import AppSettings
from app.core.settings.app_test_settings import AppTestSettings

environments: Dict[EnvTypes, Type[AppSettings]] = {
    EnvTypes.PROD: AppProdSettings,
    EnvTypes.DEV: AppDevSettings,
    EnvTypes.TEST: AppTestSettings,
}


@lru_cache()
def get_settings(app_env: EnvTypes = AppBaseSettings().app_env) -> AppSettings:
    """
    A function to retrieve chosen application settings: AppProdSettings, AppDevSettings, AppTestSettings.
    """

    log.info(f"Loading the configuration for application from the {str(app_env)} environment...")
    conf = environments[app_env]

    return conf()
