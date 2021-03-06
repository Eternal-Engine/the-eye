# type: ignore
from typing import List

import fastapi

from app.api.dependencies.authorization import retrieve_current_user_auth
from app.api.dependencies.repository import get_repository
from app.api.exceptions.http_exc_400 import http400_exc_bad_email_request, http400_exc_bad_username_request
from app.api.exceptions.http_exc_404 import http404_exc_id_not_found
from app.core.config import get_settings
from app.db.repositories.users import UsersRepository
from app.models.domain.users import User
from app.models.schemas.users import UserInResponse, UserInUpdate, UserWithToken
from app.services.authentication import check_email_is_taken, check_username_is_taken
from app.services.jwt import generate_access_token

router = fastapi.APIRouter(prefix="/users", tags=["users"])
settings = get_settings()


@router.get(path="", name="users:retrieve-all-users", response_model=List[UserInResponse])
async def retrieve_all_users(
    users_repo: UsersRepository = fastapi.Depends(get_repository(UsersRepository)),
) -> List[UserInResponse]:

    db_users = await users_repo.get_users()
    db_users_list = []

    for user in db_users:
        token = generate_access_token(
            user=user,
            secret_key=settings.secret_key,
        )
        user = UserInResponse(
            user=UserWithToken(
                username=user.username,
                email=user.email,
                is_publisher=user.is_publisher,
                is_verified=user.is_verified,
                is_active=user.is_active,
                token=token,
            ),
        )
        db_users_list.append(user)

    return db_users_list


@router.get(
    path="/{id}",
    name="users:retrieve-current-user",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def retrieve_current_user(
    id: int,
    current_user: User = fastapi.Depends(retrieve_current_user_auth()),
) -> UserInResponse:

    if id != current_user.id_:

        return await http404_exc_id_not_found(id=id)

    token = generate_access_token(
        user=current_user,
        secret_key=settings.secret_key,
    )

    return UserInResponse(
        user=UserWithToken(
            username=current_user.username,
            email=current_user.email,
            is_publisher=current_user.is_publisher,
            is_verified=current_user.is_verified,
            is_active=current_user.is_active,
            token=token,
        ),
    )


@router.put(
    path="/{id}",
    name="users:update-current-user",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_current_user(
    id: int,
    user_update: UserInUpdate = fastapi.Body(..., embed=True, alias="user"),
    current_user: User = fastapi.Depends(retrieve_current_user_auth()),
    users_repo: UsersRepository = fastapi.Depends(get_repository(UsersRepository)),
) -> UserInResponse:
    if id != current_user.id_:
        raise await http404_exc_id_not_found(id=id)

    if user_update.username and user_update.username != current_user.username:
        if await check_username_is_taken(users_repo, user_update.username):
            raise await http400_exc_bad_username_request(username=user_update.username)

    if user_update.email and user_update.email != current_user.email:
        if await check_email_is_taken(users_repo, user_update.email):
            raise await http400_exc_bad_email_request(email=user_update.email)

    updated_user = await users_repo.update_user(user=current_user, **user_update.dict())

    token = generate_access_token(
        user=updated_user,
        secret_key=settings.secret_key,
    )

    return UserInResponse(
        user=UserWithToken(
            username=updated_user.username,
            email=updated_user.email,
            is_publisher=updated_user.is_publisher,
            is_verified=updated_user.is_verified,
            is_active=updated_user.is_active,
            token=token,
        ),
    )


@router.delete(
    path="/{id}",
    name="users:delete-current-user",
    status_code=fastapi.status.HTTP_202_ACCEPTED,
)
async def delete_current_user(
    id: int,
    current_user: User = fastapi.Depends(retrieve_current_user_auth()),
    users_repo: UsersRepository = fastapi.Depends(get_repository(UsersRepository)),
) -> fastapi.responses.JSONResponse:

    if id != current_user.id_:

        raise await http404_exc_id_not_found(id=id)

    user = await users_repo.get_user_by_id(id=current_user.id_)

    await users_repo.delete_user(id=user.id_)

    return {"msg": f"User with ID {id} is successfully deleted!"}
