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
