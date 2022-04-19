import datetime

from jose import jwt as jose_jwt

from app.services import jwt as jwt_services
from app.services.config import SecuritySettings


async def test_generate_jwt_token(test_user):

    token = jwt_services.generate_jwt_token(
        jwt_data={"username": test_user.username},
        secret_key="fake-secret",
        expires_delta=datetime.timedelta(minutes=1),
    )

    assert isinstance(token, str)

    parsed_payload = jose_jwt.decode(token, "fake-secret", algorithms=[SecuritySettings.ALGORITHM_JWT])

    assert parsed_payload["username"] == "usertest"
    assert parsed_payload["sub"] == "access"


async def test_generate_access_token(test_user):

    token = jwt_services.generate_access_token(user=test_user, secret_key="fake-secret")
    parsed_payload = jose_jwt.decode(token, "fake-secret", algorithms=[SecuritySettings.ALGORITHM_JWT])

    assert parsed_payload["username"] == "usertest"
    assert parsed_payload["sub"] == "access"


def test_retrieve_access_token_from_user(test_user):

    token = jwt_services.generate_access_token(user=test_user, secret_key="fake-secret")
    username = jwt_services.retrieve_username_from_token(token, "fake-secret")

    assert username == test_user.username
