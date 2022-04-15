from app.models.domain import users as users_domain
from app.services import security


def test_verify_user_password():

    secret_key = "secret_key"
    user_password = "password"

    user_in_db = users_domain.UserInDB(
        username="johndoe",
        email="john.doe@test.com",
        salt=security.generate_layer_1_password_hash(layer_1=secret_key),
    )
    user_in_db.hashed_password = security.get_password_hash(layer_1=user_in_db.salt, password=user_password)

    assert user_in_db.salt != secret_key
    assert user_in_db.hashed_password != user_password
    assert user_in_db.hashed_password != str(user_in_db.salt + user_password)
    assert user_in_db.check_password(password=user_password) is True
