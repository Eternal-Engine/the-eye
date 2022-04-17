from app.db.repositories import users as users_repo
from app.services import authentication as auth


async def test_username_is_taken(test_pool, test_user):

    async with test_pool.acquire() as conn:

        is_username_taken = await auth.check_username_is_taken(
            repo=users_repo.UsersRepository(conn), username=test_user.username
        )

    assert is_username_taken is True


async def test_email_is_taken(test_pool, test_user):

    async with test_pool.acquire() as conn:

        is_email_taken = await auth.check_email_is_taken(repo=users_repo.UsersRepository(conn), email=test_user.email)

    assert is_email_taken is True
