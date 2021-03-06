from passlib.context import CryptContext

from app.services.config import SECURITY_SETTINGS

pwd_context_layer_1 = CryptContext(schemes=[SECURITY_SETTINGS.ALGORITHM_LAYER_1], deprecated="auto")
pwd_context_layer_2 = CryptContext(schemes=[SECURITY_SETTINGS.ALGORITHM_LAYER_2], deprecated="auto")


def generate_layer_1_password_hash(layer_1: str = SECURITY_SETTINGS.SECRET_KEY_LAYER_1) -> str:
    """
    A function to generate a hash from Bcrypt to append to the user password.
    """

    return pwd_context_layer_1.hash(secret=layer_1)  # type: ignore


def get_password_hash(layer_1: str, password: str) -> str:
    """
    A function taht adds the user's password with the layer 1 Bcrypt hash, before
    hash it for the second time using Argon2 algorithm.
    """

    return pwd_context_layer_2.hash(secret=layer_1 + password)  # type: ignore


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    A function that decodes users' password and verifies whether it is the correct password.
    """

    return pwd_context_layer_2.verify(secret=plain_password, hash=hashed_password)  # type: ignore
