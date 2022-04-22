from typing import Optional

import pydantic

from app.models.domain.journalists import Journalist
from app.models.schemas.base import IWBaseSchema  # type: ignore


class JournalistInResponse(IWBaseSchema):  # type: ignore
    profile: Journalist


class JournalistInUpdate(pydantic.BaseModel):

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
