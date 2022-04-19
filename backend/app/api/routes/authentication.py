import fastapi

from app.api.dependencies.database import get_repository
from app.api.errors.http_exc_400 import http400_exc_bad_request
from app.core.config import get_settings
from app.core.settings.app import AppSettings
from app.db.errors import EntityDoesNotExist
from app.db.repositories.users import UsersRepository
from app.models.schemas.users import UserInCreate, UserInLogin, UserInResponse, UserWithToken
from app.services.authentication import authenticate_user, check_email_is_taken, check_username_is_taken
from app.services.jwt import generate_access_token

router = fastapi.APIRouter(prefix="/authentication", tags=["Authentication"])


@router.post(
    path="/signup",
    name="auth:signup",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def signup(
    user_create: UserInCreate = fastapi.Body(..., embed=True, alias="user"),
    users_repo: UsersRepository = fastapi.Depends(get_repository(UsersRepository)),
    settings: AppSettings = fastapi.Depends(get_settings),
) -> UserInResponse:

    if await check_username_is_taken(users_repo, user_create.username):
        raise http400_exc_bad_request()

    if await check_email_is_taken(users_repo, user_create.email):
        raise http400_exc_bad_request()

    user = await users_repo.create_new_user(**user_create.dict())
    token = generate_access_token(
        user=user,
        secret_key=settings.secret_key,
    )

    return UserInResponse(
        user=UserWithToken(
            username=user.username,
            email=user.email,
            token=token,
        ),
    )


@router.post(
    path="/signin",
    name="auth:signin",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def signin(
    user_login: UserInLogin = fastapi.Body(..., embed=True, alias="user"),
    users_repo: UsersRepository = fastapi.Depends(get_repository(UsersRepository)),
    settings: AppSettings = fastapi.Depends(get_settings),
) -> UserInResponse:

    try:
        user_in_db = await authenticate_user(
            users_repo=users_repo,
            email=user_login.email,
            password=user_login.password,
        )
        if not user_in_db:
            raise http400_exc_bad_request()

    except EntityDoesNotExist as login_error:
        raise http400_exc_bad_request() from login_error

    token = generate_access_token(user=user_in_db, secret_key=settings.secret_key)

    return UserInResponse(user=UserWithToken(username=user_in_db.username, email=user_in_db.email, token=token))
