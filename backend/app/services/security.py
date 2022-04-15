from typing import Any

from passlib.context import CryptContext

pwd_context_layer_1 = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context_layer_2 = CryptContext(schemes=["argon2"], deprecated="auto")


def generate_layer_1_password_hash(layer_1: str) -> Any:
    return pwd_context_layer_1.hash(secret=layer_1)


def get_password_hash(layer_1: str, password: str) -> Any:

    return pwd_context_layer_2.hash(secret=layer_1 + password)
