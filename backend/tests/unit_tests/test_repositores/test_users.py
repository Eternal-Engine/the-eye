from app.db.repositories import users as users_repo
from app.models.schemas import users as users_schemas


async def test_create_users(test_pool):

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
    print("USER CREATED HERE")

    assert new_user.dict() == expected_data


async def test_read_all_users(test_pool):
    expected_data = {
        "id_": 1,
        "username": "johndoe",
        "email": "johndoe@test.com",
        "created_at": None,
        "updated_at": None,
    }

    async with test_pool.acquire() as conn:
        user = await users_repo.UsersRepository(conn).create_user(
            username="johndoe",
            email="johndoe@test.com",
            password="password-test",
        )

    async with test_pool.acquire() as conn:
        all_users = await users_repo.UsersRepository(conn).read_users()

    for user in all_users:
        assert user.dict(exclude={"salt", "hashed_password"}) == expected_data
