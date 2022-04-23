from typing import Optional

import pydantic

from app.models.domain.publishers import Publisher
from app.models.schemas.base import IWBaseSchema  # type: ignore


class PublisherInCreate(IWBaseSchema):
    name: Optional[str] = None
    profile_picture: Optional[str] = None
    banner: Optional[str] = None
    bio: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    office_phone_number: Optional[str] = None
    mobile_phone_number: Optional[str] = None


class PublisherInUpdate(pydantic.BaseModel):

    name: Optional[str] = None
    profile_picture: Optional[str] = None
    banner: Optional[str] = None
    bio: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    office_phone_number: Optional[str] = None
    mobile_phone_number: Optional[str] = None


class PublisherInResponse(IWBaseSchema):  # type: ignore
    publisher: Publisher
