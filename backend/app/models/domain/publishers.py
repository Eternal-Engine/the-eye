from typing import Optional

from app.models.domain.base import IWBaseModel
from app.models.mixins.date_time import DateTimeModelMixin
from app.models.mixins.identifier import IDModelMixin


class Publisher(IWBaseModel):

    name: str = ""
    profile_picture: Optional[str]
    banner: Optional[str]
    bio: str = ""
    address: str = ""
    postal_code: str = ""
    state: str = ""
    country: str = ""
    office_phone_number: str = ""
    mobile_phone_number: str = ""

    user_id: int
    # wallet_addresses: List[WalletAddress] = []
    # url_addresses: List[URLAdresses] = []
    # articles: List[Article] = []


class PublisherInDB(IDModelMixin, DateTimeModelMixin, Publisher):
    pass
