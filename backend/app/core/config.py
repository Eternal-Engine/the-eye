import logging
from functools import lru_cache
from typing import Dict, Type

from backend.app.core.settings.app_base_settings import AppBaseSettings, EnvTypes
from backend.app.core.settings.app_dev_settings import AppDevSettings
from backend.app.core.settings.app_prod_settings import AppProdSettings
from backend.app.core.settings.app_settings import AppSettings
from backend.app.core.settings.app_test_settings import AppTestSettings

log = logging.getLogger("uvicorn")
environments: Dict[EnvTypes, Type[AppSettings]] = {
    EnvTypes.PROD: AppProdSettings,
    EnvTypes.DEV: AppDevSettings,
    EnvTypes.TEST: AppTestSettings,
}


@lru_cache()
def get_settings(app_env: EnvTypes = AppBaseSettings().app_env) -> AppSettings:
    log.info("Loading config app settings from the environment...")
    conf = environments[app_env]
    return conf()
