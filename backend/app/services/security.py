from typing import Any

from passlib.context import CryptContext

pwd_context_layer_1 = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_layer_1_pwd_security(layer_1: str) -> Any:
    return pwd_context_layer_1.hash(secret=layer_1)
