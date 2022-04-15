from passlib.context import CryptContext

from app.services import security


def test_generate_layer_1_pwd_security():

    secret_key = "secret_key"

    layer_1_algorithm = CryptContext(schemes=["bcrypt"], deprecated="auto")
    salt = security.generate_layer_1_password_hash(layer_1=secret_key)

    assert isinstance(layer_1_algorithm, type(security.pwd_context_layer_1))
    assert salt != secret_key


def test_generate_layer_2_pwd_security():

    fake_layer_1_security = "fake-secret-key"
    user_password = "password"

    layer_2_algorithm = CryptContext(schemes=["argon2"], deprecated="auto")
    hashed_password = security.get_password_hash(layer_1=fake_layer_1_security, password=user_password)

    assert isinstance(layer_2_algorithm, type(security.pwd_context_layer_2))
    assert hashed_password != user_password
    assert hashed_password != fake_layer_1_security + user_password
