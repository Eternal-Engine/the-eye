from app.models.domain import base as base_model, users as users_domain
from app.models.mixins.date_time import DateTimeModelMixin
from app.models.mixins.identifier import IDModelMixin


def test_user_domain_model_construction():

    expected_attributes = {
        "username": "johndoe",
        "email": "john.doe@test.com",
        "is_premium_account": False,
        "is_publisher": False,
        "is_verified": False,
        "is_active": True,
    }
    model = base_model.IWBaseModel
    domain_user = users_domain.User(username="johndoe", email="john.doe@test.com")

    assert issubclass(type(domain_user), model)
    assert domain_user.dict() == expected_attributes


def test_user_model_for_storing_data_in_database_construction():

    expected_attributes = {
        "username": "johndoe",
        "email": "john.doe@test.com",
        "salt": "",
        "hashed_password": "",
        "is_premium_account": False,
        "is_publisher": False,
        "is_verified": False,
        "is_active": True,
        "created_at": None,
        "id_": 0,
        "updated_at": None,
    }
    user_in_db = users_domain.UserInDB(
        username="johndoe",
        email="john.doe@test.com",
    )

    domain_user = users_domain.User
    datetime_model_mixin = DateTimeModelMixin
    id_model_mixin = IDModelMixin

    assert issubclass(type(user_in_db), domain_user)
    assert issubclass(type(user_in_db), datetime_model_mixin)
    assert issubclass(type(user_in_db), id_model_mixin)
    assert user_in_db.dict() == expected_attributes
