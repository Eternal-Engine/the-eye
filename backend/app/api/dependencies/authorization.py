# type: ignore
from typing import Callable, Optional

import decouple
import fastapi

from app.api.dependencies.repository import get_repository
from app.api.exceptions.http_exc_403 import http403_exc_forbidden
from app.core.config import get_settings
from app.db.errors import EntityDoesNotExist
from app.db.repositories.users import UsersRepository
from app.models.domain.header import IWAPIKeyHeader
from app.models.domain.users import User
from app.services.jwt import retrieve_email_from_token

settings = get_settings()
HEADER_KEY = decouple.config("HEADER_KEY", cast=str)


def retrieve_current_user_auth(*, required: bool = True) -> Callable:
    return _retrieve_current_user if required else _retrieve_optional_current_user


def _get_auth_header_retriever(*, required: bool = True) -> Callable:
    return _retrieve_auth_header if required else _retrieve_optional_auth_header


def _retrieve_auth_header(
    api_key: str = fastapi.Security(IWAPIKeyHeader(name=HEADER_KEY)),
) -> str:

    try:
        token_prefix, token = api_key.split(" ")

    except ValueError as value_error:

        raise http403_exc_forbidden() from value_error

    if token_prefix != settings.jwt_token_prefix:

        raise http403_exc_forbidden()

    return token


def _retrieve_optional_auth_header(
    authentication: Optional[str] = fastapi.Security(
        IWAPIKeyHeader(name=HEADER_KEY, auto_error=False),
    ),
) -> str:
    if authentication:
        return _retrieve_auth_header(authentication)

    return ""


async def _retrieve_current_user(
    users_repo: UsersRepository = fastapi.Depends(get_repository(UsersRepository)),
    token: str = fastapi.Depends(_get_auth_header_retriever()),
) -> User:

    try:
        email = retrieve_email_from_token(token, secret_key=settings.secret_key)

    except ValueError as value_error:

        raise http403_exc_forbidden() from value_error

    try:
        return await users_repo.get_user_by_email(email=email)
    except EntityDoesNotExist as value_error:

        raise http403_exc_forbidden() from value_error


async def _retrieve_optional_current_user(
    users_repo: UsersRepository = fastapi.Depends(get_repository(UsersRepository)),
    token: str = fastapi.Depends(_get_auth_header_retriever(required=False)),
) -> Optional[User]:

    if token:
        return await _retrieve_current_user(users_repo, token)

    return None
