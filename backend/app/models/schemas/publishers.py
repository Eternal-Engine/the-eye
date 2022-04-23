from typing import Optional

import pydantic

from app.models.domain.publishers import Publisher
from app.models.schemas.base import IWBaseSchema  # type: ignore


class PublisherInResponse(IWBaseSchema):  # type: ignore
    profile: Publisher


class PublisherInUpdate(pydantic.BaseModel):

    name: Optional[str] = None
    profile_picture: Optional[str] = None
    banner: Optional[str] = None
    bio: Optional[str] = None
