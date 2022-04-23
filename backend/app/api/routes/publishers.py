from typing import List

import fastapi

from app.api.dependencies.authorization import retrieve_current_user_auth
from app.api.dependencies.publishers import retrieve_current_publisher_auth
from app.api.dependencies.repository import get_repository
from app.api.exceptions.http_exc_403 import http403_exc_forbidden
from app.api.exceptions.http_exc_404 import http404_exc_username_not_found
from app.db.repositories.publishers import PublishersRepository
from app.models.domain.publishers import Publisher
from app.models.domain.users import User
from app.models.schemas.publishers import PublisherInCreate, PublisherInResponse, PublisherInUpdate

router = fastapi.APIRouter(prefix="/publishers", tags=["publishers"])


@router.post(
    path="",
    response_model=PublisherInResponse,
    name="publishers:create-publisher-for-user-profile",
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def create_publisher_for_user_profile(
    current_user: User = fastapi.Depends(retrieve_current_user_auth()),
    publisher_create: PublisherInCreate = fastapi.Body(..., embed=True, alias="publisher"),
    publishers_repo: PublishersRepository = fastapi.Depends(get_repository(PublishersRepository)),
) -> Publisher:

    if not current_user.is_publisher:
        raise await http403_exc_forbidden()

    new_publisher = await publishers_repo.create_publisher_by_username(
        username=current_user.username, **publisher_create.dict()
    )

    return PublisherInResponse(
        publisher=Publisher(
            name=new_publisher.name,
            profile_picture=new_publisher.profile_picture,
            banner=new_publisher.banner,
            bio=new_publisher.bio,
            address=new_publisher.address,
            postal_code=new_publisher.postal_code,
            state=new_publisher.state,
            country=new_publisher.country,
            office_phone_number=new_publisher.office_phone_number,
            mobile_phone_number=new_publisher.mobile_phone_number,
            user_id=current_user.id_,
        )
    )


@router.get(path="", name="publishers:retrieve-all-publishers", response_model=List[PublisherInResponse])
async def retrieve_all_publishers(
    publishers_repo: PublishersRepository = fastapi.Depends(get_repository(PublishersRepository)),
) -> List[PublisherInResponse]:

    db_publishers = await publishers_repo.get_publishers()
    db_publishers_list = []

    for publisher in db_publishers:
        publisher = PublisherInResponse(
            publisher=Publisher(
                name=publisher.name,
                profile_picture=publisher.profile_picture,
                banner=publisher.banner,
                bio=publisher.bio,
                address=publisher.address,
                postal_code=publisher.postal_code,
                state=publisher.state,
                country=publisher.country,
                office_phone_number=publisher.office_phone_number,
                mobile_phone_number=publisher.mobile_phone_number,
                user_id=publisher.user_id,
            )
        )
        db_publishers_list.append(publisher)

    return db_publishers_list


@router.get(
    path="/publisher/{username}",
    response_model=PublisherInResponse,
    name="publishers:retrieve-current-publisher",
    status_code=fastapi.status.HTTP_200_OK,
)
async def retrieve_current_publisher(
    current_publisher: Publisher = fastapi.Depends(retrieve_current_publisher_auth),
) -> PublisherInResponse:

    return PublisherInResponse(publisher=current_publisher.publisher)


@router.put(
    path="/publisher/{username}",
    name="publishers:update-current-publisher",
    response_model=PublisherInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_current_publisher(
    username: str,
    current_user: User = fastapi.Depends(retrieve_current_user_auth()),
    current_publisher: Publisher = fastapi.Depends(retrieve_current_publisher_auth),
    publisher_update: PublisherInUpdate = fastapi.Body(..., embed=True, alias="publisher"),
    publishers_repo: PublishersRepository = fastapi.Depends(get_repository(PublishersRepository)),
) -> PublisherInResponse:  # type: ignore

    if current_publisher.publisher.user_id != current_user.id_:
        raise await http404_exc_username_not_found(username=username)  # type: ignore

    updated_publisher = await publishers_repo.update_publisher_by_user_id(
        user_id=current_publisher.publisher.user_id, **publisher_update.dict()
    )

    return PublisherInResponse(
        publisher=Publisher(
            name=updated_publisher.name,
            profile_picture=updated_publisher.profile_picture,
            bio=updated_publisher.bio,
            address=updated_publisher.address,
            postal_code=updated_publisher.postal_code,
            state=updated_publisher.state,
            country=updated_publisher.country,
            office_phone_number=updated_publisher.office_phone_number,
            mobile_phone_number=updated_publisher.mobile_phone_number,
            user_id=updated_publisher.user_id,
        )
    )
