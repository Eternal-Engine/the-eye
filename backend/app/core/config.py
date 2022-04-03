from pydantic import BaseSettings


class Settings(BaseSettings):

    ENV = "dev"
    TESTING = 1
    database_url = "sqlite:///iW_dev.sqlite3"

    def __str__(self):
        return "Application Settings"


def get_settings():

    conf = Settings

    return conf()
