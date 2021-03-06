import datetime

from jose import jwt as jose_jwt

from app.models.domain.users import UserInDB
from app.services.config import SECURITY_SETTINGS
from app.services.jwt import generate_access_token, generate_jwt_token, retrieve_email_from_token


async def test_generate_jwt_token(test_user: UserInDB):

    token = generate_jwt_token(
        jwt_data={"email": test_user.email},
        secret_key="fake-secret",
        expires_delta=datetime.timedelta(minutes=1),
    )

    assert isinstance(token, str)

    parsed_payload = jose_jwt.decode(token, "fake-secret", algorithms=[SECURITY_SETTINGS.ALGORITHM_JWT])

    assert parsed_payload["email"] == "user.test@test.com"
    assert parsed_payload["sub"] == "access"


async def test_generate_access_token(test_user: UserInDB):

    token = generate_access_token(user=test_user, secret_key="fake-secret")
    parsed_payload = jose_jwt.decode(token, "fake-secret", algorithms=[SECURITY_SETTINGS.ALGORITHM_JWT])

    assert parsed_payload["email"] == "user.test@test.com"
    assert parsed_payload["sub"] == "access"


def test_retrieve_access_token_from_user(test_user: UserInDB):

    token = generate_access_token(user=test_user, secret_key="fake-secret")
    username = retrieve_email_from_token(token, "fake-secret")

    assert username == test_user.email
