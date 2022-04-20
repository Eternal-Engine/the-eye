from app.models.domain.users import UserInDB
from app.services.security import generate_layer_1_password_hash, get_password_hash


def test_verify_user_password() -> None:

    fake_secret_key = "fake-secret-key"
    user_password = "password"

    user_in_db = UserInDB(
        username="johndoe",
        email="john.doe@test.com",
        salt=generate_layer_1_password_hash(layer_1=fake_secret_key),
    )
    user_in_db.hashed_password = get_password_hash(layer_1=user_in_db.salt, password=user_password)

    assert user_in_db.salt != fake_secret_key
    assert user_in_db.hashed_password != user_password
    assert user_in_db.hashed_password != str(user_in_db.salt + user_password)
    assert user_in_db.check_password(password=user_password) is True


def test_change_user_password() -> None:

    fake_secret_key = "fake-secret_key"
    user_password = "password"
    new_user_password = "new_password"

    user_in_db = UserInDB(
        username="johndoe",
        email="john.doe@test.com",
        salt=generate_layer_1_password_hash(layer_1=fake_secret_key),
    )
    user_in_db.hashed_password = get_password_hash(layer_1=user_in_db.salt, password=user_password)

    assert user_in_db.check_password(password=user_password) is True

    user_in_db.change_password(new_password=new_user_password)

    assert user_in_db.check_password(password=user_password) is False
    assert user_in_db.check_password(password=new_user_password) is True
