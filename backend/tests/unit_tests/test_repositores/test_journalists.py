from asyncpg import pool as asyncpg_pool

from app.db.repositories.journalists import JournalistsRepository
from app.models.domain.journalists import Journalist
from app.models.domain.users import UserInDB
from app.models.schemas.journalists import JournalistInResponse


async def test_create_journalist_with_default_create_parameter(
    test_user: UserInDB, test_pool: asyncpg_pool.Pool
) -> None:

    expected_data = {
        "journalist": {
            "first_name": "John",
            "last_name": "Doe",
            "profile_picture": "",
            "banner": "",
            "bio": "",
            "address": "",
            "postal_code": "",
            "state": "",
            "country": "",
            "office_phone_number": "",
            "mobile_phone_number": "",
            "user_id": 1,
        }
    }

    async with test_pool.acquire() as conn:
        journalists_repo = await JournalistsRepository(conn).create_journalist_by_username(
            username=test_user.username,
            first_name="John",
            last_name="Doe",
        )

    new_journalist = JournalistInResponse(
        journalist=Journalist(
            first_name=journalists_repo.first_name,
            last_name=journalists_repo.last_name,
            profile_picture=journalists_repo.profile_picture,
            banner=journalists_repo.banner,
            bio=journalists_repo.bio,
            address=journalists_repo.address,
            postal_code=journalists_repo.postal_code,
            state=journalists_repo.state,
            country=journalists_repo.country,
            office_phone_number=journalists_repo.office_phone_number,
            mobile_phone_number=journalists_repo.mobile_phone_number,
            user_id=test_user.id_,
        )
    )

    assert new_journalist.dict() == expected_data
    await test_pool.close()


async def test_read_all_journalists(
    test_user: UserInDB, test_user_journalist: UserInDB, test_pool: asyncpg_pool.Pool
) -> None:

    expected_data = [
        {
            "id_": 1,
            "first_name": "John",
            "last_name": "Doe",
            "profile_picture": "",
            "banner": "",
            "bio": "Awesome test!",
            "address": "Pytest 911",
            "postal_code": "10203",
            "state": "Berlin",
            "country": "Germany",
            "office_phone_number": "+493012335",
            "mobile_phone_number": "+4912516372932",
            "user_id": 1,
        },
        {
            "id_": 2,
            "first_name": "Maxi",
            "last_name": "Musterfrau",
            "profile_picture": "",
            "banner": "",
            "bio": "Not so awesome!",
            "address": "Unittest 987",
            "postal_code": "10407",
            "state": "Dublin",
            "country": "Ireland",
            "office_phone_number": "",
            "mobile_phone_number": "",
            "user_id": 2,
        },
    ]

    async with test_pool.acquire() as conn:
        await JournalistsRepository(conn).create_journalist_by_username(
            username=test_user.username,
            first_name="John",
            last_name="Doe",
            profile_picture="",
            banner="",
            bio="Awesome test!",
            address="Pytest 911",
            postal_code="10203",
            state="Berlin",
            country="Germany",
            office_phone_number="+493012335",
            mobile_phone_number="+4912516372932",
        )

    async with test_pool.acquire() as conn:
        await JournalistsRepository(conn).create_journalist_by_username(
            username=test_user_journalist.username,
            first_name="Maxi",
            last_name="Musterfrau",
            profile_picture="",
            banner="",
            bio="Not so awesome!",
            address="Unittest 987",
            postal_code="10407",
            state="Dublin",
            country="Ireland",
            office_phone_number="",
            mobile_phone_number="",
        )

    async with test_pool.acquire() as conn:
        db_journalists = await JournalistsRepository(conn).get_journalists()

    db_journalists[0].dict(exclude={"created_at", "updated_at"}) == expected_data[0]
    db_journalists[1].dict(exclude={"created_at", "updated_at"}) == expected_data[1]

    await test_pool.close()


async def test_read_journalist_by_user_id(test_user: UserInDB, test_pool: asyncpg_pool.Pool) -> None:

    expected_data = {
        "id_": 1,
        "first_name": "John",
        "last_name": "Doe",
        "profile_picture": "",
        "banner": "",
        "bio": "Awesome test!",
        "address": "Pytest 911",
        "postal_code": "10203",
        "state": "Berlin",
        "country": "Germany",
        "office_phone_number": "+493012335",
        "mobile_phone_number": "+4912516372932",
        "user_id": 1,
    }

    async with test_pool.acquire() as conn:
        await JournalistsRepository(conn).create_journalist_by_username(
            username=test_user.username,
            first_name="John",
            last_name="Doe",
            profile_picture="",
            banner="",
            bio="Awesome test!",
            address="Pytest 911",
            postal_code="10203",
            state="Berlin",
            country="Germany",
            office_phone_number="+493012335",
            mobile_phone_number="+4912516372932",
        )

    async with test_pool.acquire() as conn:
        db_journalist = await JournalistsRepository(conn).get_journalist_by_user_id(id=test_user.id)

    assert db_journalist.dict(exclude={"created_at", "updated_at"}) == expected_data

    await test_pool.close()


async def test_update_journalist_by_username(test_pool: asyncpg_pool.Pool, test_user: UserInDB) -> None:

    expected_data = {
        "id_": 1,
        "first_name": "John",
        "last_name": "Doe",
        "profile_picture": "home/holiday/holiday_in_dubai_2020.png",
        "banner": "",
        "bio": "",
        "address": "",
        "postal_code": "",
        "state": "",
        "country": "",
        "office_phone_number": "+493012335",
        "mobile_phone_number": "+4912516372932",
        "user_id": 1,
    }

    async with test_pool.acquire() as conn:
        new_journalist = await JournalistsRepository(conn).create_journalist_by_username(
            username=test_user.username,
            first_name="John",
            last_name="Doe",
        )

    async with test_pool.acquire() as conn:
        updated_journalist = await JournalistsRepository(conn).update_journalist_by_user_id(
            user_id=new_journalist.user_id,
            first_name="John",
            last_name="Doe",
            profile_picture="home/holiday/holiday_in_dubai_2020.png",
            banner="",
            bio="",
            address="",
            postal_code="",
            state="",
            country="",
            office_phone_number="+493012335",
            mobile_phone_number="+4912516372932",
        )

    assert updated_journalist.dict(exclude={"created_at", "updated_at"}) == expected_data

    await test_pool.close()
