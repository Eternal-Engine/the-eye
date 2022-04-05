from functools import lru_cache
from typing import Dict, Type

from app.core.settings.app_base_settings import EnvTypes
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
def get_settings():

    conf = AppSettings

    return conf()
