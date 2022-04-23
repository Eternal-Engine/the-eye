# type: ignore
import fastapi
import httpx

from app.models.domain.publishers import Publisher
from app.models.domain.users import UserInDB


async def test_get_all_publishers_successful(
    test_publisher: Publisher,
    authorized_async_client: httpx.AsyncClient,
) -> None:

    response = await authorized_async_client.get(url="api/publishers")

    assert response.status_code == fastapi.status.HTTP_200_OK
    assert response.json() == [
        {
            "publisher": {
                "name": "AxelSpringer",
                "profilePicture": "home/test/pp/AxelSpringer.png",
                "banner": "home/test/banner/AxelSPringerBanner.png",
                "bio": "Biggest media house in Europe!",
                "address": "Zimmermannstr. 50",
                "postalCode": "14350",
                "state": "Mitte",
                "country": "Germany",
                "officePhoneNumber": "+6661234567",
                "mobilePhoneNumber": "+66691112314",
                "userId": 1,
            }
        },
    ]


async def test_fail_to_retrieve_current_publisher_because_not_authorized(
    async_client: httpx.AsyncClient,
    test_user_publisher_2: UserInDB,
) -> None:

    response = await async_client.get(url=f"api/publishers/publisher/{test_user_publisher_2.username}")
    assert response.status_code == fastapi.status.HTTP_403_FORBIDDEN
