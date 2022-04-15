# type: ignore
from app.models.domain import base as base_model
from app.models.mixins.date_time import DateTimeModelMixin
from app.models.mixins.identifier import IDModelMixin
from app.services import security


class User(base_model.IWBaseModel):

    username: str
    email: str
    is_premium_account: bool = False
    is_publisher: bool = False
    is_verified: bool = False
    is_active: bool = True


class UserInDB(IDModelMixin, DateTimeModelMixin, User):

    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str) -> bool:

        return security.verify_password(self.salt + password, self.hashed_password)

    def change_password(self, new_password: str) -> None:

        self.salt = security.generate_layer_1_password_hash()
        self.hashed_password = security.get_password_hash(layer_1=self.salt, password=new_password)
