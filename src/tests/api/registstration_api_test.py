import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_registration_success(test_app: AsyncClient):
    payload = {
        "username": "api_test_user",
        "email": "api_test_user@test.test",
        "phone_number": "+375331133256",
        "password": "api_test_user_password"
    }
    response = await test_app.post("/users/signup/", json=payload)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_registration_with_duplicated_data(test_app: AsyncClient, create_test_user):
    payload = {
        "username": "api_test_user",
        "email": "api_test_user@test.test",
        "phone_number": "+375331133256",
        "password": "api_test_user_password"
    }
    response = await test_app.post("/users/signup/", json=payload)
    assert response.status_code == 409
    assert response.json() == {"detail": "A user with this data already exists."}
