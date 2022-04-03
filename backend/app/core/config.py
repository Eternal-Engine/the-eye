from pydantic import BaseSettings


class Settings(BaseSettings):

    ENV = "dev"
    TESTING = 1

    def __str__(self):
        return "Application Settings"
