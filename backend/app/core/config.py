from functools import lru_cache

from app.core.settings.app_settings import AppSettings


@lru_cache()
def get_settings():

    conf = AppSettings

    return conf()
