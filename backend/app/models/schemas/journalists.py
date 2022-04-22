from app.models.domain.journalists import Journalist
from app.models.schemas.base import IWBaseSchema  # type: ignore


class JournalistInResponse(IWBaseSchema):  # type: ignore
    profile: Journalist
