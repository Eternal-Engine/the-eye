# type: ignore
import fastapi
import httpx
from asyncpg import pool as asyncpg_pool
from fastapi import status as fastapi_exc
from starlette import status as starlette_status

from app.db.repositories import users as users_repo
from app.models.domain import users as users_domain


async def test_signup_successful(
    test_app: fastapi.FastAPI, async_client: httpx.AsyncClient, test_pool: asyncpg_pool.Pool
) -> None:

    user_signup_data = {
        "user": {
            "username": "testuser",
            "email": "test.user@test.com",
            "password": "test-password",
        }
    }

    response = await async_client.post(test_app.url_path_for("auth:signup"), json=user_signup_data)

    assert response.status_code == starlette_status.HTTP_201_CREATED

    async with test_pool.acquire() as conn:

        repo = users_repo.UsersRepository(conn)
        user = await repo.get_user_by_email(email="test.user@test.com")

        assert user.username == user_signup_data["user"]["username"]
        assert user.email == user_signup_data["user"]["email"]
        assert user.check_password(user_signup_data["user"]["password"])


async def test_failed_signup_from_taken_email(
    test_app: fastapi.FastAPI,
    async_client: httpx.AsyncClient,
    test_user: users_domain.UserInDB,
) -> None:

    user_signup_data = {
        "user": {
            "username": "usertest",
            "email": test_user.email,
            "password": "password-test",
        }
    }

    response = await async_client.post(test_app.url_path_for("auth:signup"), json=user_signup_data)

    assert response.status_code == fastapi_exc.HTTP_400_BAD_REQUEST


async def test_signin_successful(
    test_app: fastapi.FastAPI, async_client: httpx.AsyncClient, test_user: users_domain.UserInDB
) -> None:

    user_signin_data = {"user": {"email": test_user.email, "password": "password-test"}}

    response = await async_client.post(test_app.url_path_for("auth:signin"), json=user_signin_data)

    assert response.status_code == fastapi_exc.HTTP_200_OK


async def test_failed_singin_by_unmatched_password(
    test_app: fastapi.FastAPI,
    async_client: httpx.AsyncClient,
    test_user: users_domain.UserInDB,
) -> None:

    user_signin_data = {"user": {"email": test_user.email, "password": "wrong-password"}}

    response = await async_client.post(test_app.url_path_for("auth:signin"), json=user_signin_data)

    assert response.status_code == fastapi_exc.HTTP_400_BAD_REQUEST
