# fmt: off
import datetime
from typing import Any, Dict

import pydantic
from jose import JWTError as jose_jwterror, jwt as jose_jwt

from app.models.domain.users import User
from app.models.schemas.jwt import JWToken, JWTUser
from app.services.config import SECURITY_SETTINGS


def generate_jwt_token(
    *,
    jwt_data: Dict[str, str],
    secret_key: str = SECURITY_SETTINGS.SECRET_KEY_JWT,
    expires_delta: datetime.timedelta | None = None,
    ) -> Any:

    to_encode = jwt_data.copy()

    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta

    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)

    to_encode.update(JWToken(exp=expire, sub=SECURITY_SETTINGS.JWT_SUBJECT).dict())

    return jose_jwt.encode(to_encode, key=secret_key, algorithm=SECURITY_SETTINGS.ALGORITHM_JWT)


def generate_access_token(
    user: User,
    secret_key: str = SECURITY_SETTINGS.SECRET_KEY_JWT
    ) -> Any:

    return generate_jwt_token(
        jwt_data=JWTUser(email=user.email).dict(),
        secret_key=secret_key,
        expires_delta=datetime.timedelta(minutes=SECURITY_SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def retrieve_email_from_token(token: str, secret_key: str) -> str:  # type: ignore

    try:
        payload = jose_jwt.decode(token, secret_key, algorithms=[SECURITY_SETTINGS.ALGORITHM_JWT])
        return JWTUser(email=payload.get("email")).email  # type: ignore

    except jose_jwterror as token_decode_error:
        raise ValueError("Unable to decode JW-Token") from token_decode_error

    except pydantic.ValidationError as validation_error:
        raise ValueError("Invalid payload in token") from validation_error
