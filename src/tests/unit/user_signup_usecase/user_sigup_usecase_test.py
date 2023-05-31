import uuid

import pytest
from src.adapters.repositories.inmemory_user_repository import InMemoryUserRepository
from src.domain.user import User
from src.usecases.user_signup import UserSignUpUsecase


@pytest.fixture
def user_repository():
    return InMemoryUserRepository()


@pytest.fixture
def user_sign_usecase(user_repository):
    return UserSignUpUsecase(user_repository)


@pytest.mark.asyncio
async def test_expense_save_success(user_sign_usecase, user_repository):
    user = User(
        user_id=uuid.uuid4(),
        username="test_user",
        email="test_user@test.test",
        password="test_user_password",
        phone_number="+375111111111",
    )
    test_user = await user_repository.save_user(user)
    assert test_user is not None
