from app.db.repositories import users as users_repo
from app.models.schemas import users as users_schemas


async def test_create_users_function_in_users_repository(test_pool):

    expected_data = {"username": "johndoe", "email": "johndoe@test.com"}

    async with test_pool.acquire() as conn:
        user = await users_repo.UsersRepository(conn).create_user(
            username="johndoe",
            email="johndoe@test.com",
            password="password-test",
        )

        new_user = users_schemas.UserInResponse(
            username=user.username,
            email=user.email,
        )

    assert new_user.dict() == expected_data
