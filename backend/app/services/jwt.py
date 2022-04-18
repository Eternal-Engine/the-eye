import datetime
from typing import Any, Dict

import pydantic
from jose import JWTError as jose_jwterror, jwt as jose_jwt

from app.models.domain import users as users_domain
from app.models.schemas import jwt as jwt_schemas
from app.services.config import SecuritySettings

settings = SecuritySettings()


def generate_jwt_token(
    *,
    jwt_data: Dict[str, str],
    secret_key: str = settings.SECRET_KEY_JWT,
    expires_delta: datetime.timedelta | None = None,
) -> Any:

    to_encode = jwt_data.copy()

    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta

    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)

    to_encode.update(jwt_schemas.JWToken(exp=expire, sub=settings.JWT_SUBJECT).dict())

    return jose_jwt.encode(to_encode, key=secret_key, algorithm=settings.ALGORITHM_JWT)


def generate_access_token(user: users_domain.User, secret_key: str = settings.SECRET_KEY_JWT) -> Any:  # type: ignore

    return generate_jwt_token(
        jwt_data=jwt_schemas.JWTUser(username=user.username).dict(),
        secret_key=secret_key,
        expires_delta=datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def retrieve_username_from_token(token: str, secret_key: str) -> str:

    try:
        return jwt_schemas.JWTUser(**jose_jwt.decode(token, secret_key, algorithms=[settings.ALGORITHM_JWT])).username

    except jose_jwterror as token_decode_error:
        raise ValueError("Unable to decode JW-Token") from token_decode_error

    except pydantic.ValidationError as validation_error:
        raise ValueError("Invalid payload in token") from validation_error
