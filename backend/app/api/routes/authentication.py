import fastapi

from app.api.dependencies.database import get_repository
from app.core.config import get_settings
from app.core.settings.app import AppSettings
from app.db.errors import EntityDoesNotExist
from app.db.repositories import users as users_repo
from app.models.schemas import users as users_schemas
from app.services import authentication as auth_services, jwt as jwt_services

router = fastapi.APIRouter(prefix="/authentication", tags=["Authentication"])


@router.post(
    path="/signup",
    name="auth:signup",
    response_model=users_schemas.UserInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def signup(
    user_create: users_schemas.UserInCreate = fastapi.Body(..., embed=True, alias="user"),
    users_repo: users_repo.UsersRepository = fastapi.Depends(get_repository(users_repo.UsersRepository)),
    settings: AppSettings = fastapi.Depends(get_settings),
) -> users_schemas.UserInResponse:

    if await auth_services.check_username_is_taken(users_repo, user_create.username):
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Username is not available!",
        )

    if await auth_services.check_email_is_taken(users_repo, user_create.email):
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Email is not available!",
        )

    user = await users_repo.create_new_user(**user_create.dict())
    token = jwt_services.generate_access_token(
        user=user,
        secret_key=settings.secret_key,
    )

    return users_schemas.UserInResponse(
        user=users_schemas.UserWithToken(
            username=user.username,
            email=user.email,
            token=token,
        ),
    )


@router.post(
    path="/signin",
    name="auth:signin",
    response_model=users_schemas.UserInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def signin(
    user_login: users_schemas.UserInLogin = fastapi.Body(..., embed=True, alias="user"),
    users_repo: users_repo.UsersRepository = fastapi.Depends(get_repository(users_repo.UsersRepository)),
    settings: AppSettings = fastapi.Depends(get_settings),
) -> users_schemas.UserInResponse:

    login_error_exc = fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail="Incorrect login credentials, check your email or password!",
    )

    try:
        user_in_db = await auth_services.authenticate_user(
            users_repo=users_repo,
            email=user_login.email,
            password=user_login.password,
        )
        if user_in_db is False:
            raise login_error_exc

    except EntityDoesNotExist as login_error:
        raise login_error_exc from login_error

    token = jwt_services.generate_access_token(user=user_in_db, secret_key=settings.secret_key)

    return users_schemas.UserInResponse(
        user=users_schemas.UserWithToken(username=user_in_db.username, email=user_in_db.email, token=token)
    )
