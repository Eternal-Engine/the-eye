from passlib.context import CryptContext

from app.services.config import SECURITY_SETTINGS
from app.services.security import (
    generate_layer_1_password_hash,
    get_password_hash,
    pwd_context_layer_1,
    pwd_context_layer_2,
    verify_password,
)

settings = SECURITY_SETTINGS


def test_generate_layer_1_pwd_security():

    fake_secret_key = "fake_secret_key"

    layer_1_algorithm = CryptContext(schemes=[settings.ALGORITHM_LAYER_1], deprecated="auto")
    salt = generate_layer_1_password_hash(layer_1=fake_secret_key)

    assert isinstance(layer_1_algorithm, type(pwd_context_layer_1))
    assert salt != fake_secret_key


def test_generate_layer_2_pwd_security():

    fake_layer_1_security = "fake-hashing-result"
    user_password = "password"

    layer_2_algorithm = CryptContext(schemes=[settings.ALGORITHM_LAYER_2], deprecated="auto")
    hashed_password = get_password_hash(layer_1=fake_layer_1_security, password=user_password)

    assert isinstance(layer_2_algorithm, type(pwd_context_layer_2))
    assert hashed_password != user_password
    assert hashed_password != fake_layer_1_security + user_password


def test_security_system_for_user_password():

    plain_password = "password"
    fake_secret_key = "fake-secret_key"

    salt = generate_layer_1_password_hash(layer_1=fake_secret_key)
    hashed_password = get_password_hash(layer_1=salt, password=plain_password)
    verified_password = verify_password(plain_password=plain_password, hashed_password=hashed_password)
    verified_password_with_layer_one = verify_password(
        plain_password=salt + plain_password, hashed_password=hashed_password
    )

    assert hashed_password != plain_password
    assert verified_password is False
    assert verified_password_with_layer_one is True
