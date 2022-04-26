import fastapi

from app.api.dependencies.authorization import retrieve_current_user_auth
from app.api.dependencies.repository import get_repository
from app.api.exceptions.http_exc_404 import http404_exc_username_not_found
from app.db.errors import EntityDoesNotExist
from app.db.repositories.journalists import JournalistsRepository
from app.models.domain.journalists import Journalist
from app.models.domain.users import User
from app.models.schemas.journalists import JournalistInResponse


async def retrieve_current_journalist_auth(
    username: str = fastapi.Path(..., min_length=3),
    current_user: User = fastapi.Depends(retrieve_current_user_auth()),
    journalists_repo: JournalistsRepository = fastapi.Depends(get_repository(JournalistsRepository)),
) -> Journalist:

    if username == current_user.username:
        try:
            db_journalist = await journalists_repo.get_journalist_by_user_id(id=current_user.id_)

            return JournalistInResponse(journalist=Journalist(**db_journalist.dict()))

        except EntityDoesNotExist as value_error:
            raise await http404_exc_username_not_found(username=username) from value_error

    raise await http404_exc_username_not_found(username=username)
