import uuid

import pytest

from src.adapters.repositories.inmemory_user_repository import InMemoryUserRepository
from src.core.exceptions import InvalidPasswordException
from src.domain.user import User
from src.routes.user_crud.controller import LoginUserRequest
from src.usecases.password_hash import get_password_hash
from src.usecases.user_token import UserLoginUsecase


@pytest.fixture
def user_repository():
    return InMemoryUserRepository()


@pytest.fixture
def user_login_usecase(user_repository):
    return UserLoginUsecase(user_repository)


@pytest.mark.asyncio
async def test_user_login_success(user_login_usecase, user_repository):
    raw_pass = "test_user_password"
    user = User(
        user_id=uuid.uuid4(),
        username="test_user",
        email="test_user@test.test",
        password=get_password_hash(raw_pass),
        phone_number="+375111111111"
    )
    await user_repository.save_user(user)
    login = LoginUserRequest(
        login=user.username,
        password=raw_pass
    )
    login_result = await user_login_usecase.login_user(login)
    assert "access_token" in login_result
    assert "refresh_token" in login_result


@pytest.mark.asyncio
async def test_user_login_invalid_password(user_login_usecase, user_repository):
    user = User(
        user_id=uuid.uuid4(),
        username="test_user",
        email="test_user@test.test",
        password=get_password_hash("test_user_password"),
        phone_number="+375111111111",
    )
    await user_repository.save_user(user)
    with pytest.raises(InvalidPasswordException):
        login = LoginUserRequest(
            login=user.username,
            password="invalid_pass"
        )
        await user_login_usecase.login_user(login)
