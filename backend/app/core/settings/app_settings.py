import os
from typing import Any, Dict, List

from app.core.settings.app_base_settings import AppBaseSettings


class AppSettings(AppBaseSettings):

    title: str = "iWitness - Backend Production Environment Settings"
    description: str = "A backend project with FastAPI for iWitness web application."
    version: str = "0.0.0"
    debug: bool = os.getenv("DEBUG")  # type: ignore

    database_url: str = os.getenv("DATABASE_URL")
    secret_key: str = os.getenv("SECRET_KEY")

    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    api_prefix: str = "/api"

    jwt_token_prefix: str = "Token"
    allowed_hosts: List[str] = ["*"]

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
