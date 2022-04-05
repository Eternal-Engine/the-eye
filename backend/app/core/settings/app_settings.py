from typing import Any, Dict, List

from pydantic import PostgresDsn, SecretStr

from app.core.settings.app_base_settings import AppBaseSettings


class AppSettings(AppBaseSettings):

    title: str = "iWitness - Backend Production Environment Settings"
    description: str = "A backend project with FastAPI for iWitness web application."
    version: str = "0.0.0"
    debug: bool = SecretStr("DEBUG")  # type: ignore

    database_url: PostgresDsn
    secret_key: SecretStr

    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    api_prefix: str = "/api"

    jwt_token_prefix: str = "Token"
    allowed_hosts: List[str] = ["*"]

    class Config:
        env_file: str = "env/prod_env/prod.env"
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
            "database_url": self.database_url,
            "app_env": self.app_env,
        }

    def __str__(self):
        return "Application Settings"
