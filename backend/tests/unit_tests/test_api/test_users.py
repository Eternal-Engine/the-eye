import orjson

from app.api.crud import users as user_crud


async def test_create_user(async_client, monkeypatch):
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

    response = async_client.post(
        "/users/create/",
        data=orjson.dumps(test_request_payload),
    )

    assert response.status_code == 201
    assert response.json() == test_response_payload


async def test_invalid_create_user(async_client):
    response = async_client.post("/users/create/", data=orjson.dumps({}))
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
    response = async_client.post("/users/create/", data=orjson.dumps(test_request_payload))
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "field required"


def test_get_user_by_id(async_client, monkeypatch):
    test_data = {
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
        return test_data

    monkeypatch.setattr(user_crud, "get_user_by_id", mock_get_user_by_id)

    response = async_client.get("/users/id/1")

    assert response.status_code == 302
    assert response.json() == test_data


def test_get_user_by_incorrect_id_data_type(async_client, monkeypatch):

    expected_detail = [
        {
            "loc": ["path", "id"],
            "msg": "value is not a valid integer",
            "type": "type_error.integer",
        },
    ]

    async def mock_get_user_by_id(id):
        return None

    monkeypatch.setattr(user_crud, "get_user_by_id", mock_get_user_by_id)

    response = async_client.get("/users/id/1sr")

    assert response.status_code == 422
    assert response.json()["detail"] == expected_detail
