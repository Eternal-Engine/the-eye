import fastapi

from app.api.dependencies.journalists import get_journalist
from app.models.domain.journalists import Journalist
from app.models.schemas.journalists import JournalistInResponse

router = fastapi.APIRouter(prefix="/journalists", tags=["journalists"])


@router.get(
    "/{username}",
    response_model=JournalistInResponse,
)
async def retrieve_journalist_profile_by_username(
    journalist_profile: Journalist = fastapi.Depends(get_journalist),
) -> JournalistInResponse:
    print(journalist_profile)
    return JournalistInResponse(profile=journalist_profile)
