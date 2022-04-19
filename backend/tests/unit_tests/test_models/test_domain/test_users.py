from app.models.domain.base import IWBaseModel
from app.models.domain.users import User, UserInDB
from app.models.mixins.date_time import DateTimeModelMixin
from app.models.mixins.identifier import IDModelMixin


def test_user_domain_model_construction():

    expected_attributes = {
        "username": "johndoe",
        "email": "john.doe@test.com",
        # "is_premium_account": False,
        # "is_publisher": False,
        # "is_verified": False,
        # "is_active": True,
    }
    domain_base_model = IWBaseModel
    domain_user = User(username="johndoe", email="john.doe@test.com")

    assert issubclass(type(domain_user), domain_base_model)
    assert domain_user.dict() == expected_attributes


def test_user_model_for_storing_data_in_database_construction():

    expected_attributes = {
        "username": "johndoe",
        "email": "john.doe@test.com",
        "salt": "",
        "hashed_password": "",
        # "is_premium_account": False,
        # "is_publisher": False,
        # "is_verified": False,
        # "is_active": True,
        "created_at": None,
        "id_": 1,
        "updated_at": None,
    }
    user_in_db = UserInDB(
        username="johndoe",
        email="john.doe@test.com",
    )

    domain_user = User
    datetime_model_mixin = DateTimeModelMixin
    id_model_mixin = IDModelMixin

    assert issubclass(type(user_in_db), domain_user)
    assert issubclass(type(user_in_db), datetime_model_mixin)
    assert issubclass(type(user_in_db), id_model_mixin)
    assert user_in_db.dict() == expected_attributes
