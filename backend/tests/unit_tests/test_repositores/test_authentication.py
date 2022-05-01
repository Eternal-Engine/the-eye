from asyncpg import pool as asyncpg_pool

from app.db.repositories.users import UsersRepository
from app.models.domain.users import UserInDB
from app.services.authentication import check_email_is_taken, check_username_is_taken


async def test_username_is_taken(test_pool: asyncpg_pool.Pool, test_user: UserInDB) -> None:

    async with test_pool.acquire() as conn:

        is_username_taken = await check_username_is_taken(
            users_repo=UsersRepository(conn), username=test_user.username
        )

    assert is_username_taken is True
    await test_pool.close()


async def test_email_is_taken(test_pool: asyncpg_pool.Pool, test_user: UserInDB) -> None:

    async with test_pool.acquire() as conn:

        is_email_taken = await check_email_is_taken(users_repo=UsersRepository(conn), email=test_user.email)

    assert is_email_taken is True
    await test_pool.close()
