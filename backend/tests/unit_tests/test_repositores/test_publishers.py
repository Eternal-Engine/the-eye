from asyncpg import pool as asyncpg_pool

from app.db.repositories.publishers import PublishersRepository
from app.models.domain.publishers import Publisher
from app.models.domain.users import UserInDB
from app.models.schemas.publishers import PublisherInResponse


async def test_create_publisher_with_default_create_parameter(
    test_user_publisher: UserInDB, test_pool: asyncpg_pool.Pool
) -> None:

    expected_data = {
        "publisher": {
            "name": "Axel Springer",
            "profile_picture": "",
            "banner": "",
            "bio": "",
            "address": "",
            "postal_code": "",
            "state": "",
            "country": "",
            "office_phone_number": "",
            "mobile_phone_number": "",
            "user_id": test_user_publisher.id_,
        }
    }

    async with test_pool.acquire() as conn:
        publishers_repo = await PublishersRepository(conn).create_publisher_by_username(
            username=test_user_publisher.username,
            name="Axel Springer",
        )

    new_publisher = PublisherInResponse(
        publisher=Publisher(
            name=publishers_repo.name,
            profile_picture=publishers_repo.profile_picture,
            banner=publishers_repo.banner,
            bio=publishers_repo.bio,
            address=publishers_repo.address,
            postal_code=publishers_repo.postal_code,
            state=publishers_repo.state,
            country=publishers_repo.country,
            office_phone_number=publishers_repo.office_phone_number,
            mobile_phone_number=publishers_repo.mobile_phone_number,
            user_id=test_user_publisher.id_,
        )
    )

    assert new_publisher.dict() == expected_data


async def test_read_all_publishers(
    test_user_publisher: UserInDB, test_user_publisher_2: UserInDB, test_pool: asyncpg_pool.Pool
) -> None:

    expected_data = [
        {
            "id_": 1,
            "name": "Axel Springer",
            "profile_picture": "",
            "banner": "",
            "bio": "Awesome test!",
            "address": "Pytest 911",
            "postal_code": "10203",
            "state": "Berlin",
            "country": "Germany",
            "office_phone_number": "+493012335",
            "mobile_phone_number": "+4912516372932",
            "user_id": test_user_publisher.id_,
        },
        {
            "id_": 2,
            "name": "Spiegel",
            "profile_picture": "",
            "banner": "",
            "bio": "Not so awesome!",
            "address": "Unittest 987",
            "postal_code": "10407",
            "state": "Dublin",
            "country": "Ireland",
            "office_phone_number": "",
            "mobile_phone_number": "",
            "user_id": test_user_publisher_2.id_,
        },
    ]

    async with test_pool.acquire() as conn:
        await PublishersRepository(conn).create_publisher_by_username(
            username=test_user_publisher.username,
            name="Axel Springer",
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
        await PublishersRepository(conn).create_publisher_by_username(
            username=test_user_publisher_2.username,
            name="Spiegel",
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
        db_publishers = await PublishersRepository(conn).get_publishers()

    db_publishers[0].dict(exclude={"created_at", "updated_at"}) == expected_data[0]
    db_publishers[1].dict(exclude={"created_at", "updated_at"}) == expected_data[1]


async def test_read_publisher_by_user_id(test_user_publisher: UserInDB, test_pool: asyncpg_pool.Pool) -> None:

    expected_data = {
        "id_": 1,
        "name": "Axel Springer",
        "profile_picture": "",
        "banner": "",
        "bio": "Awesome test!",
        "address": "Pytest 911",
        "postal_code": "10203",
        "state": "Berlin",
        "country": "Germany",
        "office_phone_number": "+493012335",
        "mobile_phone_number": "+4912516372932",
        "user_id": test_user_publisher.id_,
    }

    async with test_pool.acquire() as conn:
        await PublishersRepository(conn).create_publisher_by_username(
            username=test_user_publisher.username,
            name="Axel Springer",
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
        db_publisher = await PublishersRepository(conn).get_publisher_by_user_id(id=test_user_publisher.id)

    assert db_publisher.dict(exclude={"created_at", "updated_at"}) == expected_data


async def test_update_publisher_by_username(test_pool: asyncpg_pool.Pool, test_user_publisher: UserInDB) -> None:

    expected_data = {
        "id_": 1,
        "name": "Axel Springer",
        "profile_picture": "home/holiday/holiday_in_dubai_2020.png",
        "banner": "",
        "bio": "",
        "address": "",
        "postal_code": "",
        "state": "",
        "country": "",
        "office_phone_number": "+493012335",
        "mobile_phone_number": "+4912516372932",
        "user_id": test_user_publisher.id_,
    }

    async with test_pool.acquire() as conn:
        await PublishersRepository(conn).create_publisher_by_username(
            username=test_user_publisher.username,
            name="Axel Springer",
        )

    async with test_pool.acquire() as conn:
        db_publisher = await PublishersRepository(conn).get_publisher_by_user_id(id=test_user_publisher.id)

    async with test_pool.acquire() as conn:
        updated_publisher = await PublishersRepository(conn).update_publisher_by_user_id(
            user_id=db_publisher.user_id,
            name="Axel Springer",
            profile_picture="home/holiday/holiday_in_dubai_2020.png",
            office_phone_number="+493012335",
            mobile_phone_number="+4912516372932",
        )

    assert updated_publisher.dict(exclude={"created_at", "updated_at"}) == expected_data
