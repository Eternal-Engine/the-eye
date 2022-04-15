# type: ignore

from passlib.context import CryptContext
from pydantic import SecretStr

pwd_context_layer_1 = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context_layer_2 = CryptContext(schemes=["argon2"], deprecated="auto")


def generate_layer_1_password_hash(layer_1: str = SecretStr("SECRET_KEY").get_secret_value()) -> str:
    """
    A function to generate a hash from Bcrypt to append to the user password.
    """
    return pwd_context_layer_1.hash(secret=layer_1)


def get_password_hash(layer_1: str, password: str) -> str:
    """
    A function taht adds the user's password with the layer 1 Bcrypt hash, before
    hash it for the second time using Argon2 algorithm.
    """

    return pwd_context_layer_2.hash(secret=layer_1 + password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    A function that decodes users' password and verifies whether it is the correct password.
    """

    return pwd_context_layer_2.verify(secret=plain_password, hash=hashed_password)
