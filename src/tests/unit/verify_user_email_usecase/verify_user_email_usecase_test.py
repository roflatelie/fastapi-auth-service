import uuid

import pytest

from src.adapters.repositories.inmemory_user_repository import InMemoryUserRepository
from src.domain.user import User
from src.usecases.verify_user_email import VerifyUserEmailUsecase


@pytest.fixture
def user_repository():
    return InMemoryUserRepository()


@pytest.fixture
def verify_email_usecase(user_repository):
    return VerifyUserEmailUsecase(user_repository)


@pytest.mark.asyncio
async def test_update_email_verification_success(verify_email_usecase, user_repository):
    user = User(
        user_id=uuid.uuid4(),
        username="test_user",
        email="test_user@test.test",
        password="password",
        phone_number="+375111111111"
    )
    await user_repository.save_user(user)

    result = await verify_email_usecase.update_email_verification(user.user_id)

    assert result == {"success": True}


@pytest.mark.asyncio
async def test_update_email_verification_exception(verify_email_usecase, user_repository):
    user = User(
        user_id=uuid.uuid4(),
        username="test_user",
        email="test_user@test.test",
        password="password",
        phone_number="+375111111111"
    )
    await user_repository.save_user(user)
    result = await verify_email_usecase.update_email_verification(uuid.uuid4())
    assert result == {"success": False}
