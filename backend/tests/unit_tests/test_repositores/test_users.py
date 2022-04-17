from app.db.repositories import users as users_repo
from app.models.schemas import users as users_schemas


async def test_create_users(test_pool):

    expected_data = {"username": "johndoe", "email": "johndoe@test.com"}

    async with test_pool.acquire() as conn:
        user = await users_repo.UsersRepository(conn).create_new_user(
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
        user = await users_repo.UsersRepository(conn).create_new_user(
            username="johndoe",
            email="johndoe@test.com",
            password="password-test",
        )

    async with test_pool.acquire() as conn:
        all_users_in_db = await users_repo.UsersRepository(conn).get_users()

    for user_in_db in all_users_in_db:
        assert user_in_db.dict(exclude={"salt", "hashed_password"}) == expected_data
        assert user_in_db.dict(exclude={"salt", "hashed_password"}) == user.dict(
            exclude={"id", "salt", "hashed_password"}
        )


async def test_read_user_by_id(test_pool, test_user):

    expected_data = {
        "id_": 1,
        "username": "usertest",
        "email": "user.test@test.com",
    }

    async with test_pool.acquire() as conn:
        user_in_db = await users_repo.UsersRepository(conn).get_user_by_id(user_id=test_user.id)

    assert user_in_db.dict(exclude={"salt", "hashed_password", "created_at", "updated_at"}) == expected_data


async def test_read_user_by_username(test_pool, test_user):

    expected_data = {
        "id_": 1,
        "username": "usertest",
        "email": "user.test@test.com",
    }

    async with test_pool.acquire() as conn:
        user_in_db = await users_repo.UsersRepository(conn).get_user_by_username(username=test_user.username)

    assert user_in_db.dict(exclude={"salt", "hashed_password", "created_at", "updated_at"}) == expected_data


async def test_read_user_by_email(test_pool, test_user):

    expected_data = {
        "id_": 1,
        "username": "usertest",
        "email": "user.test@test.com",
    }

    async with test_pool.acquire() as conn:
        user_in_db = await users_repo.UsersRepository(conn).get_user_by_email(user_email=test_user.email)

    assert user_in_db.dict(exclude={"salt", "hashed_password", "created_at", "updated_at"}) == expected_data


async def test_update_user_by_id(test_pool, test_user):

    expected_data = {
        "id_": 1,
        "username": "updated-testuser",
        "email": "updated-test.user@test.com",
    }
    current_user = test_user

    async with test_pool.acquire() as conn:
        updated_user = await users_repo.UsersRepository(conn).revise_user_by_id(
            user=current_user,
            username="updated-testuser",
            email="updated-test.user@test.com",
            password="updated-password",
        )

    assert updated_user.dict(exclude={"salt", "hashed_password", "created_at", "updated_at"}) == expected_data


async def test_update_user_by_username(test_pool, test_user):

    expected_data = {
        "id_": 1,
        "username": "updated-testuser",
        "email": "updated-test.user@test.com",
    }
    current_user = test_user

    async with test_pool.acquire() as conn:
        updated_user = await users_repo.UsersRepository(conn).revise_user_by_username(
            user=current_user,
            username="updated-testuser",
            email="updated-test.user@test.com",
            password="updated-password",
        )

    assert updated_user.dict(exclude={"salt", "hashed_password", "created_at", "updated_at"}) == expected_data


async def test_delete_user_by_id(test_pool, test_user):

    current_user = test_user

    async with test_pool.acquire() as conn:
        deleted_user = await users_repo.UsersRepository(conn).remove_user_by_id(user_id=current_user.id)

    assert deleted_user != current_user
    assert deleted_user == "User is successfully deleted from database!"


async def test_delete_user_by_username(test_pool, test_user):

    current_user = test_user

    async with test_pool.acquire() as conn:
        deleted_user = await users_repo.UsersRepository(conn).remove_user_by_username(username=current_user.username)

    assert deleted_user != current_user
    assert deleted_user == "User is successfully deleted from database!"
