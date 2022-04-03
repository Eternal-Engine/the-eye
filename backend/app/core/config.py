from pydantic import BaseSettings


class Settings(BaseSettings):

    ENV = "dev"
    database_url = "sqlite:///iW_dev.sqlite3"
    title = "iWitness - Backend Development Application"
    description = "A backend project with FastAPI for iWitness web application."
    version = "0.0.0"
    debug = True
    docs_url = "/docs"
    openapi_prefix = ""
    openapi_url = "/openapi.json"
    redoc_url = "/redoc"

    @property
    def fastapi_kwargs(self):
        return {
            "title": self.title,
            "description": self.description,
            "version": self.version,
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
        }

    def __str__(self):
        return "Application Settings"


def get_settings():

    conf = Settings

    return conf()
