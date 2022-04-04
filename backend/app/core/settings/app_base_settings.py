from enum import Enum

from pydantic import BaseSettings


class EnvTypes(Enum):

    PROD: str = "prod"
    DEV: str = "dev"
    TEST: str = "test"

    def describe(self):
        """
        A function to inspect all EnvTypes attributes.
        """
        return f"{self.name}: {self.value}"

    def __str__(self):
        return f"{self.value.capitalize()} environment type"


class AppBaseSettings(BaseSettings):

    app_env: EnvTypes = EnvTypes.PROD

    def __str__(self):
        return "Base Settings for App Settings"
