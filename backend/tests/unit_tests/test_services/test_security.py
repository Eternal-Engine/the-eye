from passlib.context import CryptContext

from app.services import security


def test_generate_layer_1_pwd_security():

    secret_key = "secret_key"

    layer_1_algorithm = CryptContext(schemes=["bcrypt"], deprecated="auto")
    salt = security.generate_layer_1_pwd_security(layer_1=secret_key)

    assert isinstance(layer_1_algorithm, type(security.pwd_context_layer_1))
    assert salt != secret_key
