from typing import List

import fastapi

from app.api.dependencies.authorization import retrieve_current_user_auth
from app.api.dependencies.journalists import retrieve_current_journalist_auth
from app.api.dependencies.repository import get_repository
from app.api.exceptions.http_exc_403 import http403_exc_forbidden
from app.api.exceptions.http_exc_404 import http404_exc_username_not_found
from app.db.repositories.journalists import JournalistsRepository
from app.models.domain.journalists import Journalist
from app.models.domain.users import User
from app.models.schemas.journalists import JournalistInCreate, JournalistInResponse, JournalistInUpdate

router = fastapi.APIRouter(prefix="/journalists", tags=["journalists"])


@router.post(
    path="",
    response_model=JournalistInResponse,
    name="journalists:create-journalist-for-user-profile",
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def create_journalist_for_user_profile(
    current_user: User = fastapi.Depends(retrieve_current_user_auth()),
    journalist_create: JournalistInCreate = fastapi.Body(..., embed=True, alias="journalist"),
    journalists_repo: JournalistsRepository = fastapi.Depends(get_repository(JournalistsRepository)),
) -> JournalistInResponse:  # type: ignore

    if current_user.is_publisher:
        raise await http403_exc_forbidden()

    new_journalist = await journalists_repo.create_journalist_by_username(
        username=current_user.username, **journalist_create.dict()
    )

    return JournalistInResponse(
        journalist=Journalist(
            first_name=new_journalist.first_name,
            last_name=new_journalist.last_name,
            profile_picture=new_journalist.profile_picture,
            banner=new_journalist.banner,
            bio=new_journalist.bio,
            address=new_journalist.address,
            postal_code=new_journalist.postal_code,
            state=new_journalist.state,
            country=new_journalist.country,
            office_phone_number=new_journalist.office_phone_number,
            mobile_phone_number=new_journalist.mobile_phone_number,
            user_id=current_user.id_,
        )
    )


@router.get(path="", name="journalists:retrieve-all-journalists", response_model=List[JournalistInResponse])
async def retrieve_all_journalists(
    journalists_repo: JournalistsRepository = fastapi.Depends(get_repository(JournalistsRepository)),
) -> List[JournalistInResponse]:

    db_journalists = await journalists_repo.get_journalists()
    db_journalists_list = []

    for journalist in db_journalists:
        journalist = JournalistInResponse(
            journalist=Journalist(
                first_name=journalist.first_name,
                last_name=journalist.last_name,
                profile_picture=journalist.profile_picture,
                banner=journalist.banner,
                bio=journalist.bio,
                address=journalist.address,
                postal_code=journalist.postal_code,
                state=journalist.state,
                country=journalist.country,
                office_phone_number=journalist.office_phone_number,
                mobile_phone_number=journalist.mobile_phone_number,
                user_id=journalist.user_id,
            )
        )
        db_journalists_list.append(journalist)

    return db_journalists_list


@router.get(
    path="/journalist/{username}",
    response_model=JournalistInResponse,
    name="journalists:retrieve-current-journalist",
    status_code=fastapi.status.HTTP_200_OK,
)
async def retrieve_current_journalist(
    current_journalist: Journalist = fastapi.Depends(retrieve_current_journalist_auth),
) -> JournalistInResponse:  # type: ignore

    return JournalistInResponse(journalist=current_journalist.journalist)


@router.put(
    path="/journalist/{username}",
    name="journalists:update-current-journalist",
    response_model=JournalistInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_current_journalist(
    username: str,
    current_user: User = fastapi.Depends(retrieve_current_user_auth()),
    current_journalist: Journalist = fastapi.Depends(retrieve_current_journalist_auth),
    journalist_update: JournalistInUpdate = fastapi.Body(..., embed=True, alias="journalist"),
    journalists_repo: JournalistsRepository = fastapi.Depends(get_repository(JournalistsRepository)),
) -> JournalistInResponse:  # type: ignore

    if current_journalist.journalist.user_id != current_user.id_:
        raise await http404_exc_username_not_found(username=username)  # type: ignore

    updated_journalist = await journalists_repo.update_journalist_by_user_id(
        user_id=current_journalist.journalist.user_id, **journalist_update.dict()
    )

    return JournalistInResponse(
        journalist=Journalist(
            first_name=updated_journalist.first_name,
            last_name=updated_journalist.last_name,
            profile_picture=updated_journalist.profile_picture,
            bio=updated_journalist.bio,
            address=updated_journalist.address,
            postal_code=updated_journalist.postal_code,
            state=updated_journalist.state,
            country=updated_journalist.country,
            office_phone_number=updated_journalist.office_phone_number,
            mobile_phone_number=updated_journalist.mobile_phone_number,
            user_id=updated_journalist.user_id,
        )
    )
