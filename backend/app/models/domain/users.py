from app.models.domain.base import IWBaseModel
from app.models.mixins.date_time import DateTimeModelMixin
from app.models.mixins.identifier import IDModelMixin
from app.services.security import generate_layer_1_password_hash, get_password_hash, verify_password


class User(IWBaseModel):

    username: str
    email: str
    is_publisher: bool = False
    is_verified: bool = False
    is_active: bool = True


class UserInDB(IDModelMixin, DateTimeModelMixin, User):

    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str) -> bool:

        return verify_password(plain_password=self.salt + password, hashed_password=self.hashed_password)

    def change_password(self, new_password: str) -> None:

        self.salt = generate_layer_1_password_hash()
        self.hashed_password = get_password_hash(layer_1=self.salt, password=new_password)
