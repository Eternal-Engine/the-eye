from typing import Optional

from app.models.domain.users import User
from app.models.mixins.date_time import DateTimeModelMixin
from app.models.mixins.identifier import IDModelMixin


class Journalist(User):

    first_name: str = ""
    last_name: str = ""
    profile_picture: Optional[str]
    bio: str = ""

    user_id: int
    # wallet_addresses: List[WalletAddress] = []
    # url_addresses: List[URLAdresses] = []
    # articles: List[Article] = []


class JournalistInDB(IDModelMixin, DateTimeModelMixin, Journalist):
    pass
