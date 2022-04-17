import enum

import pydantic


class EnvTypes(enum.Enum):
    """
    The class that stores the 3 types of environment: production, development, test.
    """

    PROD: str = "production"
    DEV: str = "development"
    TEST: str = "test"

    def describe(self):
        """
        A function to inspect all EnvTypes attributes.
        """
        return f"{self.name}: {self.value}"

    def __str__(self):
        return self.value


class AppBaseSettings(pydantic.BaseSettings):
    """
    A class that is utilized as a container for setting up
    the environment for the application settings.
    """

    app_env: EnvTypes = EnvTypes.PROD

    def __str__(self):
        return "Base Settings for App Settings"
