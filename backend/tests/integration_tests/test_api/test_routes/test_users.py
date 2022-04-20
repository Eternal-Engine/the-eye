# type: ignore
import fastapi
import httpx
from asyncpg import pool as asyncpg_pool

from app.db.repositories.users import UsersRepository
from app.models.domain.users import UserInDB
from app.models.schemas.users import UserInResponse


async def test_retrieve_current_user_successful(
    authorized_async_client: httpx.AsyncClient,
    test_user: UserInDB,
) -> None:

    response = await authorized_async_client.get(url="api/user?id=1")
    assert response.status_code == fastapi.status.HTTP_200_OK

    user_profile = UserInResponse(**response.json())
    assert user_profile.user.email == test_user.email


async def test_fail_to_retrieve_current_user_by_invalid_id_not_found(
    authorized_async_client: httpx.AsyncClient,
) -> None:

    response = await authorized_async_client.get(url="api/user?id=2")
    assert response.status_code == fastapi.status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "errors": ["Either the user with ID 2 is deleted, or you are not authorized; Check your authorization!"]
    }


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

    response = await authorized_async_client.put(url="api/user/update?id=1", json=updated_user_data)
    assert response.status_code == fastapi.status.HTTP_200_OK

    updated_user = UserInResponse(**response.json()).dict()

    assert updated_user != test_user
    assert "token" in updated_user["user"]


async def test_user_update_password_successful(
    authorized_async_client: httpx.AsyncClient,
    test_pool: asyncpg_pool.Pool,
) -> None:

    response = await authorized_async_client.put(
        url="api/user/update?id=1",
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

    response = await authorized_async_client.delete(url="api/user/delete?id=1")

    assert response.status_code == fastapi.status.HTTP_202_ACCEPTED
    assert response.json() == {"msg": "User with ID 1 is successfully deleted!"}
