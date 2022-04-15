# type: ignore
from app.models import base_models
from app.models.mixins.date_time import DateTimeModelMixin
from app.models.mixins.identifier import IDModelMixin


class User(base_models.IWBaseModel):

    username: str
    email: str
    is_premium_account: bool = False
    is_publisher: bool = False
    is_verified: bool = False
    is_active: bool = True


class UserInDB(IDModelMixin, DateTimeModelMixin, User):

    salt: str = ""
    hashed_password: str = ""
