import pytest
from asyncpg import pool as asyncpg_pool

from app.db.repositories.users import UsersRepository
from app.models.domain.users import UserInDB
from app.models.schemas.users import UserInResponse, UserWithToken


async def test_create_user_journalist_with_default_create_parameter(test_pool: asyncpg_pool.Pool) -> None:

    expected_data = {
        "user": {
            "username": "johndoe",
            "email": "johndoe@test.com",
            "is_publisher": False,
            "is_verified": False,
            "is_active": True,
            "token": "fake-token",
        }
    }

    async with test_pool.acquire() as conn:
        users_repo = await UsersRepository(conn).create_user(
            username="johndoe",
            email="johndoe@test.com",
            password="password-test",
        )

    new_user = UserInResponse(
        user=UserWithToken(
            username=users_repo.username,
            email=users_repo.email,
            is_publisher=users_repo.is_publisher,
            is_verified=users_repo.is_verified,
            is_active=users_repo.is_active,
            token="fake-token",
        ),
    )

    assert new_user.dict() == expected_data


async def test_create_user_publisher(test_pool: asyncpg_pool.Pool) -> None:

    expected_data = {
        "user": {
            "username": "johndoe",
            "email": "johndoe@test.com",
            "is_publisher": True,
            "is_verified": False,
            "is_active": True,
            "token": "fake-token",
        }
    }

    async with test_pool.acquire() as conn:
        users_repo = await UsersRepository(conn).create_user(
            username="johndoe",
            email="johndoe@test.com",
            password="password-test",
            is_publisher=True,
        )

    new_user = UserInResponse(
        user=UserWithToken(
            username=users_repo.username,
            email=users_repo.email,
            is_publisher=users_repo.is_publisher,
            is_verified=users_repo.is_verified,
            is_active=users_repo.is_active,
            token="fake-token",
        ),
    )

    assert new_user.dict() == expected_data


async def test_read_all_users(test_pool: asyncpg_pool.Pool) -> None:
    expected_data = {
        "id_": 1,
        "username": "johndoe",
        "email": "johndoe@test.com",
        "is_publisher": False,
        "is_verified": False,
        "is_active": True,
        "created_at": None,
        "updated_at": None,
    }

    async with test_pool.acquire() as conn:
        users_repo = await UsersRepository(conn).create_user(
            username="johndoe",
            email="johndoe@test.com",
            password="password-test",
            is_publisher=False,
        )

    async with test_pool.acquire() as conn:
        all_users_in_db = await UsersRepository(conn).get_users()

    for user_in_db in all_users_in_db:
        assert user_in_db.dict(exclude={"salt", "hashed_password"}) == expected_data
        assert user_in_db.dict(exclude={"salt", "hashed_password"}) == users_repo.dict(
            exclude={"id", "salt", "hashed_password"}
        )


async def test_read_user_by_id(test_pool: asyncpg_pool.Pool, test_user: UserInDB) -> None:

    expected_data = {
        "id_": 1,
        "username": "usertest",
        "email": "user.test@test.com",
        "is_publisher": False,
        "is_verified": False,
        "is_active": True,
    }

    async with test_pool.acquire() as conn:
        user_in_db = await UsersRepository(conn).get_user_by_id(id=test_user.id)

    assert user_in_db.dict(exclude={"salt", "hashed_password", "created_at", "updated_at"}) == expected_data


async def test_read_user_by_invalid_id_raise_exception(test_pool: asyncpg_pool.Pool) -> None:

    invalid_id = 999

    with pytest.raises(Exception, match=f"User with id {invalid_id} does not exist!"):
        async with test_pool.acquire() as conn:
            await UsersRepository(conn).get_user_by_id(id=invalid_id)


async def test_read_user_by_username(test_pool: asyncpg_pool.Pool, test_user: UserInDB) -> None:

    expected_data = {
        "id_": 1,
        "username": "usertest",
        "email": "user.test@test.com",
        "is_publisher": False,
        "is_verified": False,
        "is_active": True,
    }

    async with test_pool.acquire() as conn:
        user_in_db = await UsersRepository(conn).get_user_by_username(username=test_user.username)

    assert user_in_db.dict(exclude={"salt", "hashed_password", "created_at", "updated_at"}) == expected_data


async def test_read_user_by_invalid_username_raise_exception(test_pool: asyncpg_pool.Pool) -> None:

    invalid_username = "invalidusername"

    with pytest.raises(Exception, match=f"User with username {invalid_username} does not exist!"):
        async with test_pool.acquire() as conn:
            await UsersRepository(conn).get_user_by_username(username=invalid_username)


async def test_read_user_by_email(test_pool: asyncpg_pool.Pool, test_user: UserInDB) -> None:

    expected_data = {
        "id_": 1,
        "username": "usertest",
        "email": "user.test@test.com",
        "is_publisher": False,
        "is_verified": False,
        "is_active": True,
    }

    async with test_pool.acquire() as conn:
        user_in_db = await UsersRepository(conn).get_user_by_email(email=test_user.email)

    assert user_in_db.dict(exclude={"salt", "hashed_password", "created_at", "updated_at"}) == expected_data


async def test_read_user_by_invalid_email_raise_exception(test_pool: asyncpg_pool.Pool) -> None:

    invalid_email = "invalid.email@test.com"

    with pytest.raises(Exception, match=f"User with email {invalid_email} does not exist!"):
        async with test_pool.acquire() as conn:
            await UsersRepository(conn).get_user_by_email(email=invalid_email)


async def test_update_user(test_pool: asyncpg_pool.Pool, test_user: UserInDB) -> None:

    expected_data = {
        "id_": 1,
        "username": "updated-testuser",
        "email": "updated-test.user@test.com",
        "is_publisher": False,
        "is_verified": False,
        "is_active": True,
    }
    current_user = test_user

    async with test_pool.acquire() as conn:
        updated_user = await UsersRepository(conn).update_user(
            user=current_user,
            username="updated-testuser",
            email="updated-test.user@test.com",
            password="updated-password",
        )

    assert updated_user.dict(exclude={"salt", "hashed_password", "created_at", "updated_at"}) == expected_data


async def test_delete_user_by_id(test_pool: asyncpg_pool.Pool, test_user: UserInDB) -> None:

    async with test_pool.acquire() as conn:
        deleted_user = await UsersRepository(conn).delete_user(id=test_user.id)

    assert deleted_user != test_user
    assert deleted_user is None
