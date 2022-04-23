from typing import Optional

import fastapi

from app.api.dependencies.authorization import retrieve_current_user_auth
from app.api.dependencies.repository import get_repository
from app.api.exceptions.http_exc_404 import http404_exc_username_not_found
from app.db.errors import EntityDoesNotExist
from app.db.repositories.journalists import JournalistsRepository
from app.models.domain.journalists import Journalist
from app.models.domain.users import User


async def get_journalist(
    username: str = fastapi.Path(..., min_length=1),
    user: Optional[User] = fastapi.Depends(retrieve_current_user_auth(required=False)),
    profiles_repo: JournalistsRepository = fastapi.Depends(get_repository(JournalistsRepository)),
) -> Journalist:

    try:
        return await profiles_repo.create_journalist_profile_from_getting_user_by_username(
            username=username,
            journalist_profile=user,
        )

    except EntityDoesNotExist as value_error:
        raise await http404_exc_username_not_found(username=username) from value_error
