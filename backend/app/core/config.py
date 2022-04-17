from functools import lru_cache
from typing import Dict, Type

from app.core.logging import log
from app.core.settings.app import AppSettings
from app.core.settings.base import AppBaseSettings, EnvTypes
from app.core.settings.development import AppDevSettings
from app.core.settings.production import AppProdSettings
from app.core.settings.staging import AppStagingSettings

environments: Dict[EnvTypes, Type[AppSettings]] = {
    EnvTypes.PROD: AppProdSettings,
    EnvTypes.DEV: AppDevSettings,
    EnvTypes.TEST: AppStagingSettings,
}


@lru_cache()
def get_settings(app_env: EnvTypes = AppBaseSettings().app_env) -> AppSettings:
    """
    A function to retrieve chosen application settings: AppProdSettings, AppDevSettings, AppTestSettings.
    """

    log.info(f"Loading the configuration for application from the {str(app_env)} environment...")
    conf = environments[app_env]

    return conf()
