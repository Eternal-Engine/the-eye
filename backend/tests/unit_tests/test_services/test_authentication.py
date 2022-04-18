from app.db.repositories import users as users_repo
from app.services.authentication import (  # type: ignore
    authenticate_user,
    check_email_is_taken,
    check_username_is_taken,
)


async def test_email_is_taken(test_pool, test_user):

    async with test_pool.acquire() as conn:
        is_email_taken = await check_email_is_taken(repo=users_repo.UsersRepository(conn), email=test_user.email)

    assert is_email_taken is True


async def test_email_is_not_taken(test_pool):

    async with test_pool.acquire() as conn:
        is_email_taken = await check_email_is_taken(
            repo=users_repo.UsersRepository(conn), email="email.still.available@test.com"
        )

    assert is_email_taken is False


async def test_username_is_taken(test_pool, test_user):

    async with test_pool.acquire() as conn:
        is_username_taken = await check_username_is_taken(
            repo=users_repo.UsersRepository(conn), username=test_user.username
        )

    assert is_username_taken is True


async def test_username_is_not_taken(test_pool):

    async with test_pool.acquire() as conn:
        is_email_taken = await check_username_is_taken(
            repo=users_repo.UsersRepository(conn), username="availableusername"
        )

    assert is_email_taken is False


async def test_user_authentication_failed_with_no_user_found(test_pool):

    async with test_pool.acquire() as conn:
        is_user_authenticated = await authenticate_user(
            repo=users_repo.UsersRepository(conn), username="invalidusername", password="fake-password"
        )

    assert is_user_authenticated is False


async def test_user_authentication_failed_with_unmatched_password(test_pool, test_user):

    async with test_pool.acquire() as conn:
        is_user_authenticated = await authenticate_user(
            repo=users_repo.UsersRepository(conn), username=test_user.username, password="fake-password"
        )

    assert is_user_authenticated is False


async def test_user_successfully_authenticated(test_pool, test_user):

    async with test_pool.acquire() as conn:
        is_user_authenticated = await authenticate_user(
            repo=users_repo.UsersRepository(conn), username=test_user.username, password="password-test"
        )

    assert is_user_authenticated.dict(exclude={"created_at", "updated_at"}) == test_user.dict(
        exclude={"id", "created_at", "updated_at"}
    )
