# type: ignore
import fastapi
import httpx
from asyncpg import pool as asyncpg_pool

from app.db.repositories.users import UsersRepository
from app.models.domain.users import UserInDB


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

    assert response.status_code == fastapi.status.HTTP_201_CREATED

    async with test_pool.acquire() as conn:

        users_repo = UsersRepository(conn)
        user = await users_repo.get_user_by_email(email="test.user@test.com")

        assert user.username == user_signup_data["user"]["username"]
        assert user.email == user_signup_data["user"]["email"]
        assert user.check_password(user_signup_data["user"]["password"])


async def test_failed_signup_from_taken_email(
    test_app: fastapi.FastAPI,
    async_client: httpx.AsyncClient,
    test_user: UserInDB,
) -> None:

    user_signup_data = {
        "user": {
            "username": "availableusertest",
            "email": test_user.email,
            "password": "password-test",
        }
    }

    response = await async_client.post(test_app.url_path_for("auth:signup"), json=user_signup_data)

    assert response.status_code == fastapi.status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "errors": ["The email user.test@test.com is taken! Be creative and choose another one!"]
    }


async def test_failed_signup_from_taken_username(
    test_app: fastapi.FastAPI,
    async_client: httpx.AsyncClient,
    test_user: UserInDB,
) -> None:

    user_signup_data = {
        "user": {
            "username": test_user.username,
            "email": "available.testuser@test.com",
            "password": "password-test",
        }
    }

    response = await async_client.post(test_app.url_path_for("auth:signup"), json=user_signup_data)

    assert response.status_code == fastapi.status.HTTP_400_BAD_REQUEST
    assert response.json() == {"errors": ["The username usertest is taken! Be creative and choose another one!"]}


async def test_signin_successful(
    test_app: fastapi.FastAPI, async_client: httpx.AsyncClient, test_user: UserInDB
) -> None:

    user_signin_data = {"user": {"email": test_user.email, "password": "password-test"}}

    response = await async_client.post(test_app.url_path_for("auth:signin"), json=user_signin_data)

    assert response.status_code == fastapi.status.HTTP_200_OK


async def test_failed_singin_by_unmatched_password(
    test_app: fastapi.FastAPI,
    async_client: httpx.AsyncClient,
    test_user: UserInDB,
) -> None:

    user_signin_data = {"user": {"email": test_user.email, "password": "wrong-password"}}

    response = await async_client.post(test_app.url_path_for("auth:signin"), json=user_signin_data)

    assert response.status_code == fastapi.status.HTTP_400_BAD_REQUEST
    assert response.json() == {"errors": ["Login failed! Re-check heck your email and password!"]}
