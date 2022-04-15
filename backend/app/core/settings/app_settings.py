import logging
import os
from typing import Any, Dict, List, Tuple

from app.core.settings.app_base_settings import AppBaseSettings


class AppSettings(AppBaseSettings):
    """
    The parent class for all 3 types of aplication settings
    to set up the FastAPI instance with a customized configuration.
    """

    title: str = "iWitness - Backend Production Environment Settings"
    description: str = "A backend project with FastAPI for iWitness web application."
    version: str = "0.0.0"
    debug: bool = False

    database_url: str = os.getenv("DATABASE_URL")
    secret_key: str = os.getenv("SECRET_KEY")

    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    api_prefix: str = "/api"

    jwt_token_prefix: str = "Token"
    allowed_hosts: List[str] = ["*"]
    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    max_connection_count: int = 10
    min_connection_count: int = 10

    class Config:
        env_file = "env/.env.production"
        validate_assignment: bool = True

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "description": self.description,
            "version": self.version,
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "openapi_prefix": self.openapi_prefix,
            "api_prefix": self.api_prefix,
            "app_env": self.app_env,
        }

    def __str__(self):
        return "Application Settings"
