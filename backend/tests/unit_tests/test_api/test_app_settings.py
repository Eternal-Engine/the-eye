async def test_async_retrieve_app_settings_route(async_client):

    expected = {"environment": "prod"}

    response = async_client.get("/api/app_settings/")

    assert response.status_code == 200
    assert response.json() == expected
