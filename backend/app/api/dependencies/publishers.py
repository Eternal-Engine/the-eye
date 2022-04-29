# type: ignore
import fastapi

from app.api.dependencies.authorization import retrieve_current_user_auth
from app.api.dependencies.repository import get_repository
from app.api.exceptions.http_exc_404 import http404_exc_username_not_found
from app.db.errors import EntityDoesNotExist
from app.db.repositories.publishers import PublishersRepository
from app.models.domain.publishers import Publisher
from app.models.domain.users import User
from app.models.schemas.publishers import PublisherInResponse


async def retrieve_current_publisher_auth(
    username: str = fastapi.Path(..., min_length=3),
    current_user: User = fastapi.Depends(retrieve_current_user_auth()),
    publishers_repo: PublishersRepository = fastapi.Depends(get_repository(PublishersRepository)),
) -> Publisher:

    if username == current_user.username:
        try:
            db_publisher = await publishers_repo.get_publisher_by_user_id(id=current_user.id_)

            return PublisherInResponse(publisher=Publisher(**db_publisher.dict()))

        except EntityDoesNotExist as value_error:
            raise await http404_exc_username_not_found(username=username) from value_error

    raise await http404_exc_username_not_found(username=username)
