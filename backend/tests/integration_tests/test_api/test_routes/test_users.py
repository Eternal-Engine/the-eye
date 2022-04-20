# type: ignore
import fastapi
import httpx
from asyncpg import pool as asyncpg_pool

from app.db.repositories.users import UsersRepository
from app.models.domain.users import UserInDB
from app.models.schemas.users import UserInResponse


async def test_retrieve_current_user(
    test_app: fastapi.FastAPI,
    authorized_async_client: httpx.AsyncClient,
    test_user: UserInDB,
) -> None:

    response = await authorized_async_client.get(test_app.url_path_for("users:get-current-user"))
    assert response.status_code == fastapi.status.HTTP_200_OK

    user_profile = UserInResponse(**response.json())
    assert user_profile.user.email == test_user.email


async def test_update_current_user(
    test_app: fastapi.FastAPI,
    test_user: UserInDB,
    authorized_async_client: httpx.AsyncClient,
) -> None:

    updated_user_data = {
        "user": {
            "username": "updated-testusername",
            "email": "updated.test.user@test.com",
        }
    }

    response = await authorized_async_client.put(
        test_app.url_path_for("users:update-current-user"), json=updated_user_data
    )
    assert response.status_code == fastapi.status.HTTP_200_OK

    updated_user = UserInResponse(**response.json()).dict()

    assert updated_user != test_user
    assert "token" in updated_user["user"]


async def test_user_update_password(
    test_app: fastapi.FastAPI,
    authorized_async_client: httpx.AsyncClient,
    test_pool: asyncpg_pool.Pool,
) -> None:

    response = await authorized_async_client.put(
        test_app.url_path_for("users:update-current-user"),
        json={"user": {"password": "new_password"}},
    )
    assert response.status_code == fastapi.status.HTTP_200_OK
    updated_user = UserInResponse(**response.json())

    async with test_pool.acquire() as conn:
        users_repo = UsersRepository(conn)
        user_in_db = await users_repo.get_user_by_email(email=updated_user.user.email)

    assert user_in_db.check_password("new_password")


async def test_fail_update_current_user_by_taken_username(
    test_app: fastapi.FastAPI,
    authorized_async_client: httpx.AsyncClient,
    test_user: httpx.AsyncClient,
    test_pool: asyncpg_pool.Pool,
) -> None:
    other_user = {
        "username": "available_username",
        "email": "available.email@test.com",
        "password": "password",
    }

    other_user.update({"username": test_user.username})

    async with test_pool.acquire() as conn:
        users_repo = UsersRepository(conn)
        await users_repo.create_user(**other_user)

    response = await authorized_async_client.put(
        test_app.url_path_for("users:update-current-user"),
        json={"user": other_user},
    )

    assert response.status_code == fastapi.status.HTTP_400_BAD_REQUEST
