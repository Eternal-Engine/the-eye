import fastapi

from app.api.dependencies.authorization import retrieve_current_user_auth
from app.api.dependencies.journalists import get_journalist
from app.api.dependencies.repository import get_repository
from app.api.exceptions.http_exc_404 import http404_exc_username_not_found
from app.db.repositories.journalists import JournalistsRepository
from app.models.domain.journalists import Journalist
from app.models.domain.users import User
from app.models.schemas.journalists import JournalistInResponse, JournalistInUpdate

router = fastapi.APIRouter(prefix="/journalists", tags=["journalists"])


@router.get("/{username}", response_model=JournalistInResponse, name="journalists:get-journalist-profile")
async def retrieve_journalist_profile_by_username(
    journalist_profile: Journalist = fastapi.Depends(get_journalist),
) -> JournalistInResponse:

    return JournalistInResponse(profile=journalist_profile)


@router.put(
    path="/{username}",
    name="journalists:update-journalist",
    response_model=JournalistInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_journalist_profile_by_username(
    username: str,
    journalist_update: JournalistInUpdate = fastapi.Body(..., embed=True, alias="journalist"),
    current_user: User = fastapi.Depends(retrieve_current_user_auth()),
    current_journalist: User = fastapi.Depends(get_journalist),
    journalists_repo: JournalistsRepository = fastapi.Depends(get_repository(JournalistsRepository)),
) -> JournalistInResponse:  # type: ignore

    if current_journalist.user_id != current_user.id_:
        raise await http404_exc_username_not_found(username=username)  # type: ignore

    updated_journalist = await journalists_repo.update_journalist(
        journalist=current_journalist, **journalist_update.dict()
    )

    return JournalistInResponse(
        profile=Journalist(
            first_name=updated_journalist.first_name,
            last_name=updated_journalist.last_name,
            profile_picture=updated_journalist.profile_picture,
            bio=updated_journalist.bio,
            user_id=updated_journalist.user_id,
        )
    )
