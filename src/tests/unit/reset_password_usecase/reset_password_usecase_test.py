import uuid

import pytest

from src.adapters.repositories.inmemory_user_repository import InMemoryUserRepository
from src.domain.user import User
from src.routes.user_crud.controller import LoginUserRequest
from src.usecases.password_hash import get_password_hash
from src.usecases.reset_password import ResetPasswordUsecase


@pytest.fixture
def user_repository():
    return InMemoryUserRepository()


@pytest.fixture
def reset_password_usecase(user_repository):
    return ResetPasswordUsecase(user_repository)


@pytest.mark.asyncio
async def test_update_password_success(reset_password_usecase, user_repository):
    user = User(
        user_id=uuid.uuid4(),
        username="test_user",
        email="test_user@test.test",
        password=get_password_hash("test_user_password"),
        phone_number="+375111111111"
    )
    await user_repository.save_user(user)
    new_password = "new_test_password"
    result = await reset_password_usecase.update_password(new_password, user.user_id)
    assert result == {"success": True}
    login = LoginUserRequest(
        login=user.username,
        password=new_password
    )
    updated_user = await user_repository.select_user(login)
    assert updated_user.password == new_password
