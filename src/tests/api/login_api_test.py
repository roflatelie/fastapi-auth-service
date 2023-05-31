import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_sing_in_with_username_success(test_app: AsyncClient, create_test_user):
    payload = {
        "login": "api_test_user",
        "password": "api_test_user_password"
    }
    response = await test_app.post("/users/login/", json=payload)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_sing_in_with_email_success(test_app: AsyncClient, create_test_user):
    payload = {
        "login": "api_test_user@test.test",
        "password": "api_test_user_password"
    }
    response = await test_app.post("/users/login/", json=payload)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_sing_in_with_phone_number_success(test_app: AsyncClient, create_test_user):
    payload = {
        "login": "+375331133256",
        "password": "api_test_user_password"
    }
    response = await test_app.post("/users/login/", json=payload)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_sing_in_with_invalid_login(test_app: AsyncClient, create_test_user):
    payload = {
        "login": "+375331133256234",
        "password": "api_test_user_password"
    }
    response = await test_app.post("/users/login/", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "There is no user with this data: +375331133256234"}


@pytest.mark.asyncio
async def test_sing_in_with_invalid_password(test_app: AsyncClient, create_test_user):
    payload = {
        "login": "+375331133256",
        "password": "api_test_user_password1111"
    }
    response = await test_app.post("/users/login/", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect password."}
