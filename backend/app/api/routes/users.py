from typing import Any

import fastapi

from app.api.dependencies.authorization import retrieve_current_user_auth
from app.api.dependencies.database import get_repository
from app.core.config import get_settings
from app.core.settings.app import AppSettings
from app.db.repositories.users import UsersRepository
from app.models.domain.users import User
from app.models.schemas.users import UserInResponse, UserInUpdate, UserWithToken
from app.services.authentication import check_email_is_taken, check_username_is_taken
from app.services.jwt import generate_access_token

router = fastapi.APIRouter(prefix="/users", tags=["User"])


@router.get(
    path="/user",
    name="users:get-current-user",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def retrieve_current_user(
    user: User = fastapi.Depends(retrieve_current_user_auth()),
    settings: AppSettings = fastapi.Depends(get_settings),
) -> UserInResponse:
    token = generate_access_token(
        user,
        settings.secret_key,
    )
    return UserInResponse(
        user=UserWithToken(
            username=user.username,
            email=user.email,
            token=token,
        ),
    )


@router.put(
    path="/update",
    name="users:update-current-user",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_current_user(
    user_update: UserInUpdate = fastapi.Body(..., embed=True, alias="user"),
    current_user: User = fastapi.Depends(retrieve_current_user_auth()),
    users_repo: UsersRepository = fastapi.Depends(get_repository(UsersRepository)),
    settings: AppSettings = fastapi.Depends(get_settings),
) -> UserInResponse:
    if user_update.username and user_update.username != current_user.username:
        if await check_username_is_taken(users_repo, user_update.username):
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                detail="Username is taken!",
            )

    if user_update.email and user_update.email != current_user.email:
        if await check_email_is_taken(users_repo, user_update.email):
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                detail="Email is taken!",
            )

    user = await users_repo.update_user(user=current_user, **user_update.dict())

    token = generate_access_token(
        user,
        settings.secret_key,
    )

    return UserInResponse(
        user=UserWithToken(
            username=user.username,
            email=user.email,
            token=token,
        ),
    )


@router.delete(
    path="/delete",
    name="users:delete-current-user",
    status_code=fastapi.status.HTTP_202_ACCEPTED,
)
async def delete_current_user(
    current_user: User = fastapi.Depends(retrieve_current_user_auth()),
    users_repo: UsersRepository = fastapi.Depends(get_repository(UsersRepository)),
) -> Any:

    user = await users_repo.get_user_by_id(id=current_user.id_)  # type: ignore

    return await users_repo.delete_user(id=user.id_)  # type: ignore
