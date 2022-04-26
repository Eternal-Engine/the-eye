# type: ignore
import fastapi
import httpx

from app.models.domain.journalists import JournalistInDB
from app.models.domain.users import UserInDB
from app.resources.http_exc_details import http_404_details


async def test_get_all_journalists_successful(
    test_user_publisher_2: UserInDB,
    authorized_async_client: httpx.AsyncClient,
) -> None:

    new_publisher = {
        "journalist": {
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
            "user_id": test_user_publisher_2.id_,
        }
    }

    response = await authorized_async_client.post(url="api/journalists", json=new_publisher)
    assert response.status_code == fastapi.status.HTTP_201_CREATED

    response = await authorized_async_client.get(url="api/journalists")

    assert response.status_code == fastapi.status.HTTP_200_OK

    assert response.json() == [
        {
            "journalist": {
                "firstName": "John",
                "lastName": "Doe",
                "profilePicture": "home/holiday/holiday_in_dubai_2020.png",
                "banner": "",
                "bio": "",
                "address": "",
                "postalCode": "",
                "state": "",
                "country": "",
                "officePhoneNumber": "+493012335",
                "mobilePhoneNumber": "+4912516372932",
                "userId": 2,
            }
        },
    ]


async def test_retrieve_current_journalist_successful(
    authorized_async_client: httpx.AsyncClient,
    test_journalist: JournalistInDB,
    test_user: UserInDB,
) -> None:

    response = await authorized_async_client.get(url=f"api/journalists/journalist/{test_user.username}")
    assert response.status_code == fastapi.status.HTTP_200_OK
    assert response.json() == {
        "journalist": {
            "firstName": "Tester",
            "lastName": "Journalist",
            "profilePicture": "home/test/pp/journalist.png",
            "banner": "home/test/banner/journalist_banner.png",
            "bio": "Awesome super journalist",
            "address": "Secretstreet 666",
            "postalCode": "13055",
            "state": "Kuta",
            "country": "Dreamland",
            "officePhoneNumber": "+666",
            "mobilePhoneNumber": "+666911",
            "userId": test_journalist.user_id,
        }
    }


async def test_fail_to_retrieve_current_journalist_with_invalid_username(
    authorized_async_client: httpx.AsyncClient,
    test_journalist: JournalistInDB,
    test_user: UserInDB,
) -> None:

    exc_msg = http_404_details(username=f"invalid{test_user.username}")

    response = await authorized_async_client.get(url=f"api/journalists/journalist/invalid{test_user.username}")
    assert response.status_code == fastapi.status.HTTP_404_NOT_FOUND
    assert response.json() != test_journalist.dict()
    assert response.json() == {"errors": [exc_msg]}


async def test_update_current_journalist_successful(
    test_user: UserInDB,
    test_journalist: JournalistInDB,
    authorized_async_client: httpx.AsyncClient,
) -> None:

    updated_journalist_data = {
        "journalist": {
            "first_name": "John Doe",
            "last_name": "Doe",
            "banner": None,
            "bio": "Updated awesome journalist!",
            "profile_picture": "home/holiday/holiday_in_dubai_2020.png",
            "office_phone_number": "+493012335",
            "mobile_phone_number": "+4912516372932",
        }
    }

    response = await authorized_async_client.put(
        url=f"api/journalists/journalist/{test_user.username}", json=updated_journalist_data
    )
    assert response.status_code == fastapi.status.HTTP_200_OK
    assert response.json() == {
        "journalist": {
            "firstName": "John Doe",
            "lastName": "Doe",
            "profilePicture": "home/holiday/holiday_in_dubai_2020.png",
            "banner": None,
            "bio": "Updated awesome journalist!",
            "address": test_journalist.address,
            "postalCode": test_journalist.postal_code,
            "state": test_journalist.state,
            "country": test_journalist.country,
            "officePhoneNumber": "+493012335",
            "mobilePhoneNumber": "+4912516372932",
            "userId": test_user.id_,
        }
    }
