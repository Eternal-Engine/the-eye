from functools import lru_cache

from app.core.settings.app_settings import AppSettings

app_environments: dict


@lru_cache()
def get_settings():

    conf = AppSettings

    return conf()
