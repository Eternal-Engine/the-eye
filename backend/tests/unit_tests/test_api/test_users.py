# fmt: off
import orjson
import pytest

from app.api.crud import users as user_crud


async def test_create_users(async_client, monkeypatch):
    test_request_payload = {
        "username": "johndoe",
        "email": "john.doe@example.com",
        "password": "yxcasdqwe+hashed",
        "is_publisher": False,
        "is_premium_account": False,
        "is_verified": False,
        "is_active": True,
    }
    test_response_payload = {
        "id": 1,
        "username": "johndoe",
        "email": "john.doe@example.com",
        "is_publisher": False,
        "is_premium_account": False,
        "is_verified": False,
        "is_active": True,
        "created_at": None,
        "updated_at": None,
        "last_logged_in_at": None,
        "username_updated_at": None,
        "email_updated_at": None,
        "password_updated_at": None,
    }

    async def mock_create_user(payload):
        return 1

    monkeypatch.setattr(user_crud, "create_user", mock_create_user)

    response = await async_client.post(
        "/api/users/create",
        data=orjson.dumps(test_request_payload),
    )

    assert response.status_code == 201
    assert response.json() == test_response_payload


async def test_invalid_create_user(async_client):

    response = await async_client.post("/api/users/create", data=orjson.dumps({}))

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "username"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "email"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "password"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }

    test_request_payload = {
        "username": "johndoe",
    }

    response = await async_client.post("/api/users/create", data=orjson.dumps(test_request_payload))
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "field required"


async def test_async_retrieve_all_users(async_client, monkeypatch):

    expected_data = [
        {
            "id": 1,
            "username": "johndoe",
            "email": "john.doe@example.com",
            "is_publisher": False,
            "is_premium_account": False,
            "is_verified": False,
            "is_active": True,
            "created_at": "2022-04-12T17:16:25.194495",
            "updated_at": "2022-04-12T17:16:25.194495",
            "last_logged_in_at": "2022-04-12T17:16:25.194495",
            "username_updated_at": "2022-04-12T17:16:25.194495",
            "email_updated_at": "2022-04-12T17:16:25.194495",
            "password_updated_at": "2022-04-12T17:16:25.194495",
        },
        {
            "id": 2,
            "username": "maximusterfrau",
            "email": "maxi.musterfrau@example.com",
            "is_publisher": False,
            "is_premium_account": False,
            "is_verified": False,
            "is_active": True,
            "created_at": "2022-04-12T17:16:25.194495",
            "updated_at": "2022-04-12T17:16:25.194495",
            "last_logged_in_at": "2022-05-12T19:20:30.194495",
            "username_updated_at": "2022-05-12T19:20:30.194495",
            "email_updated_at": "2022-05-12T19:20:30.194495",
            "password_updated_at": "2022-05-12T19:20:30.194495",
        },
    ]

    async def mock_get_all_users():
        return expected_data

    monkeypatch.setattr(user_crud, "get_all_users", mock_get_all_users)

    response = await async_client.get("/api/users")

    assert response.status_code == 200
    assert response.json() == expected_data


async def test_async_retrieve_user_by_id(async_client, monkeypatch):
    expected_data = {
        "id": 1,
        "username": "johndoe",
        "email": "john.doe@example.com",
        "is_publisher": False,
        "is_premium_account": False,
        "is_verified": False,
        "is_active": True,
        "created_at": "2022-04-12T17:16:25.194495",
        "updated_at": "2022-04-12T17:16:25.194495",
        "last_logged_in_at": "2022-04-12T17:16:25.194495",
        "username_updated_at": "2022-04-12T17:16:25.194495",
        "email_updated_at": "2022-04-12T17:16:25.194495",
        "password_updated_at": "2022-04-12T17:16:25.194495",
    }

    async def mock_get_user_by_id(id):
        return expected_data

    monkeypatch.setattr(user_crud, "get_user_by_id", mock_get_user_by_id)

    response = async_client.get("/api/users/id/1")

    assert response.status_code == 200
    assert response.json() == expected_data


async def test_retrieve_user_by_incorrect_id_data_type(async_client, monkeypatch):

    expected_detail = [
        {
            "loc": ["path", "user_id"],
            "msg": "value is not a valid integer",
            "type": "type_error.integer",
        },
    ]

    async def mock_get_user_by_id(id):
        return None

    monkeypatch.setattr(user_crud, "get_user_by_id", mock_get_user_by_id)

    response = async_client.get("/api/users/id/1sr")

    assert response.status_code == 422
    assert response.json()["detail"] == expected_detail


async def test_async_update_user(async_client, monkeypatch):
    expected_updated_data = {
        "id": 1,
        "username": "maxmusterman",
        "email": "max.musterman@gmail.com",
        "is_publisher": False,
        "is_premium_account": False,
        "is_verified": False,
        "is_active": True,
        "created_at": None,
        "updated_at": None,
        "last_logged_in_at": None,
        "username_updated_at": None,
        "email_updated_at": None,
        "password_updated_at": None,
    }

    async def mock_get_user_by_id(id):
        return True

    monkeypatch.setattr(user_crud, "get_user_by_id", mock_get_user_by_id)

    async def mock_update_user(id, payload):
        return 1

    monkeypatch.setattr(user_crud, "update_user", mock_update_user)

    response = async_client.put("/api/users/id/1", data=orjson.dumps(expected_updated_data))

    assert response.status_code == 200
    assert response.json() == expected_updated_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 404],
        [1, {"email": "max.musterman@example.com"}, 404],
        [999, {"username": "foo", "email": "max.musterman@example.com"}, 404],
    ],
)
async def test_async_update_user_with_invalid_input(async_client, monkeypatch, id, payload, status_code):
    async def mock_get_user_by_id(id):
        return None

    monkeypatch.setattr(user_crud, "get_user_by_id", mock_get_user_by_id)

    response = async_client.put(
        f"/users/id/{id}/",
        data=orjson.dumps(payload),
    )

    assert response.status_code == status_code


async def test_async_remove_user(async_client, monkeypatch):
    expected_data = {
        "id": 1,
        "username": "maxmusterman",
        "email": "max.musterman@gmail.com",
        "is_publisher": False,
        "is_premium_account": False,
        "is_verified": False,
        "is_active": True,
        "created_at": None,
        "updated_at": None,
        "last_logged_in_at": None,
        "username_updated_at": None,
        "email_updated_at": None,
        "password_updated_at": None,
    }

    async def mock_get_user_by_id(id):
        return expected_data

    monkeypatch.setattr(user_crud, "get_user_by_id", mock_get_user_by_id)

    async def mock_delete_user(id):
        return id

    monkeypatch.setattr(user_crud, "delete_user", mock_delete_user)

    response = async_client.delete("/api/users/id/1")

    assert response.status_code == 202
    assert response.json() == expected_data


async def test_async_remove_user_by_incorrect_id_data_type(async_client, monkeypatch):
    expected_data = [
        {
            "loc": ["path", "user_id"],
            "msg": "value is not a valid integer",
            "type": "type_error.integer",
        },
    ]

    async def mock_get_user_by_id(id):
        return None

    monkeypatch.setattr(user_crud, "get_user_by_id", mock_get_user_by_id)

    response = async_client.delete("/api/users/id/66G")
    assert response.status_code == 422
    assert response.json()["detail"] == expected_data
