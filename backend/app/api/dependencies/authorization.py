from typing import Callable, Optional

import decouple
import fastapi

from app.api.dependencies.database import get_repository
from app.core.config import get_settings
from app.core.settings.app import AppSettings
from app.db.errors import EntityDoesNotExist
from app.db.repositories import users as users_repo
from app.models.domain import header as header_domain, users as users_domain
from app.services import jwt as jwt_services
from app.services.config import SecuritySettings

SECURITY_SETTINGS = SecuritySettings()
HEADER_KEY = decouple.config("HEADER_KEY", cast=str)


def retrieve_current_user_auth(*, required: bool = True) -> Callable:
    return _retrieve_current_user if required else _retrieve_optional_current_user


def _get_auth_header_retriever(*, required: bool = True) -> Callable:
    return _retrieve_auth_header if required else _retrieve_optional_auth_header


def _retrieve_auth_header(
    api_key: str = fastapi.Security(header_domain.IWAPIKeyHeader(name=HEADER_KEY)),
    settings: AppSettings = fastapi.Depends(get_settings),
) -> str:

    try:
        token_prefix, token = api_key.split(" ")

    except ValueError as value_error:

        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN, detail="Authorization prefix is unsupported!"
        ) from value_error

    if token_prefix != settings.jwt_token_prefix:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="Authorization prefix is unsupported!",
        )

    return token


def _retrieve_optional_auth_header(
    auth: Optional[str] = fastapi.Security(
        header_domain.IWAPIKeyHeader(name=HEADER_KEY, auto_error=False),
    ),
    settings: AppSettings = fastapi.Depends(get_settings),
) -> str:
    if auth:
        return _retrieve_auth_header(auth, settings)

    return ""


async def _retrieve_current_user(
    users_repo: users_repo.UsersRepository = fastapi.Depends(get_repository(users_repo.UsersRepository)),
    token: str = fastapi.Depends(_get_auth_header_retriever()),
    settings: AppSettings = fastapi.Depends(get_settings),
) -> users_domain.User:

    settings.secret_key = SECURITY_SETTINGS.SECRET_KEY_JWT

    try:
        username = jwt_services.retrieve_username_from_token(token, secret_key=settings.secret_key)

    except ValueError as value_error:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="Unable to validate credentials!",
        ) from value_error

    try:
        return await users_repo.get_user_by_username(username=username)
    except EntityDoesNotExist as value_error:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="Unable to validate credentials!",
        ) from value_error


async def _retrieve_optional_current_user(
    repo: users_repo.UsersRepository = fastapi.Depends(get_repository(users_repo.UsersRepository)),
    token: str = fastapi.Depends(_get_auth_header_retriever(required=False)),
    settings: AppSettings = fastapi.Depends(get_settings),
) -> Optional[users_domain.User]:

    if token:
        return await _retrieve_current_user(repo, token, settings)

    return None
