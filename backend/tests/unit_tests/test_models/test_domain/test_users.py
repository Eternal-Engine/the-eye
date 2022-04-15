from app.models import base_models
from app.models.domain import users as users_domain


def test_user_domain_model_construction():

    expected_attributes = {
        "username": "johndoe",
        "email": "john.doe@test.com",
        "is_premium_account": False,
        "is_publisher": False,
        "is_verified": False,
        "is_active": True,
    }
    base_model = base_models.IWBaseModel
    user_domain = users_domain.User(username="johndoe", email="john.doe@test.com")

    assert issubclass(type(user_domain), base_model)
    assert user_domain.dict() == expected_attributes
