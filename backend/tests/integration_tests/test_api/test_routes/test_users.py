# type: ignore
import fastapi
import httpx
from asyncpg import pool as asyncpg_pool

from app.db.repositories.users import UsersRepository
from app.models.domain.users import UserInDB
from app.models.schemas.users import UserInResponse
from app.resources.http_exc_details import http_404_details


async def test_get_all_users_successful(
    authorized_async_client: httpx.AsyncClient,
    test_pool: asyncpg_pool.Pool,
) -> None:

    second_user_signup_data = {
        "user": {
            "username": "testuser2",
            "email": "test.user2@test.com",
            "password": "test-password2",
        }
    }

    response = await authorized_async_client.post(url="api/auth/signup", json=second_user_signup_data)

    assert response.status_code == fastapi.status.HTTP_201_CREATED

    response = await authorized_async_client.get(url="api/users")
    users_list = response.json()

    for user in users_list:
        user["user"]["token"] = "fake-token"

    assert response.status_code == fastapi.status.HTTP_200_OK

    assert users_list == [
        {
            "user": {
                "username": "usertest",
                "email": "user.test@test.com",
                "token": "fake-token",
                "isPublisher": False,
                "isVerified": False,
                "isActive": True,
            }
        },
        {
            "user": {
                "username": "testuser2",
                "email": "test.user2@test.com",
                "token": "fake-token",
                "isPublisher": False,
                "isVerified": False,
                "isActive": True,
            }
        },
    ]


async def test_retrieve_current_user_successful(
    authorized_async_client: httpx.AsyncClient,
    test_user: UserInDB,
) -> None:

    response = await authorized_async_client.get(url="api/users/user/1")
    assert response.status_code == fastapi.status.HTTP_200_OK

    db_user = UserInResponse(**response.json())
    assert db_user.user.email == test_user.email


async def test_fail_to_retrieve_current_user_by_invalid_id_not_found(
    authorized_async_client: httpx.AsyncClient,
) -> None:

    response = await authorized_async_client.get(url="api/users/user/2")
    assert response.status_code == fastapi.status.HTTP_404_NOT_FOUND
    assert response.json() == {"errors": [http_404_details(id=2)]}


async def test_update_current_user_username_and_email_successful(
    test_user: UserInDB,
    authorized_async_client: httpx.AsyncClient,
) -> None:

    updated_user_data = {
        "user": {
            "username": "updated-testusername",
            "email": "updated.test.user@test.com",
        }
    }

    response = await authorized_async_client.put(url="api/users/user/1", json=updated_user_data)
    assert response.status_code == fastapi.status.HTTP_200_OK

    updated_user = UserInResponse(**response.json()).dict()

    assert updated_user != test_user
    assert "token" in updated_user["user"]


async def test_user_update_password_successful(
    authorized_async_client: httpx.AsyncClient,
    test_pool: asyncpg_pool.Pool,
) -> None:

    response = await authorized_async_client.put(
        url="api/users/user/1",
        json={"user": {"password": "new_password"}},
    )
    assert response.status_code == fastapi.status.HTTP_200_OK
    updated_user = UserInResponse(**response.json())

    async with test_pool.acquire() as conn:
        users_repo = UsersRepository(conn)
        user_in_db = await users_repo.get_user_by_email(email=updated_user.user.email)

    assert user_in_db.check_password("new_password")


async def test_delete_user_successfully_return_http202(
    authorized_async_client: httpx.AsyncClient,
    test_user: httpx.AsyncClient,
    test_pool: asyncpg_pool.Pool,
) -> None:

    async with test_pool.acquire() as conn:
        current_user = UsersRepository(conn)
        await current_user.get_user_by_email(email=test_user.email)

    response = await authorized_async_client.delete(url="api/users/user/1")

    assert response.status_code == fastapi.status.HTTP_202_ACCEPTED
    assert response.json() == {"msg": "User with ID 1 is successfully deleted!"}
