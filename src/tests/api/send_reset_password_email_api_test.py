import pytest
from httpx import AsyncClient

from src.main import app
from src.tests.api.dependency_overrider import DependencyOverrider
from src.tests.api.override_dependencies import override_send_email_dependency_success, \
    override_send_email_dependency_exception
from src.adapters.repositories.aws_ses_repository import AWSSesRepository


@pytest.mark.asyncio
async def test_send_verification_email_success(test_app: AsyncClient, create_test_user):
    payload = {
        "login": "+375331133256",
        "password": "api_test_user_password"
    }
    async with DependencyOverrider(app, overrides={
        AWSSesRepository.send_verification_email: override_send_email_dependency_success}):
        token = await test_app.post("/users/login/", json=payload)
        headers = {'Authorization': 'Bearer ' + token.json().get("access_token")}
        response = await test_app.get("/users/account/reset_password/", headers=headers)
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_send_verification_email_processing_exception(test_app: AsyncClient, create_test_user):
    payload = {
        "login": "+375331133256",
        "password": "api_test_user_password"
    }
    async with DependencyOverrider(app, overrides={
        AWSSesRepository.send_verification_email: override_send_email_dependency_exception}):
        token = await test_app.post("/users/login/", json=payload)
        headers = {'Authorization': 'Bearer ' + token.json().get("access_token")}
        response = await test_app.get("/users/account/reset_password/", headers=headers)
        assert response.status_code == 400
        assert response.json() == {"detail": "Please try later."}


@pytest.mark.asyncio
async def test_send_verification_email_invalid_token(test_app: AsyncClient, create_test_user):
    payload = {
        "login": "+37533113325",
        "password": "api_test_user_password"
    }
    async with DependencyOverrider(app, overrides={
        AWSSesRepository.send_verification_email: override_send_email_dependency_success}):
        token = await test_app.post("/users/login/", json=payload)
        headers = {'Authorization': 'Bearer ' + token.json().get("access_token")}
        response = await test_app.get("/users/account/reset_password/", headers=headers)
        assert response.status_code == 401
