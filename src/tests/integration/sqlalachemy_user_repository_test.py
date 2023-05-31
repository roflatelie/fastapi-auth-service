import uuid

import pytest
import pytest_asyncio
from sqlalchemy import delete

from src.adapters.orm_engines import models
from src.adapters.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.core.exceptions import DuplicatedEntryError, UserNotFoundException
from src.domain.user import User
from src.routes.user_crud.controller import LoginUserRequest


@pytest_asyncio.fixture
async def user_repository(session) -> SQLAlchemyUserRepository:
    repository = SQLAlchemyUserRepository(session)
    yield repository
    await repository.session.execute(delete(models.User))


@pytest_asyncio.fixture
async def create_test_user(user_repository: SQLAlchemyUserRepository):
    user = User(
        user_id=uuid.uuid4(),
        username="test_fixture_user",
        email="test_fixture_user@test.test",
        password="test_fixture_user_password",
        phone_number="+375112222222"
    )
    await user_repository.save_user(user)
    return user.user_id


@pytest.mark.asyncio
async def test_user_registration_success(user_repository: SQLAlchemyUserRepository):
    user = User(
        user_id=uuid.uuid4(),
        username="test_user",
        email="test_user@test.test",
        password="test_user_password",
        phone_number="+375111111111"
    )
    test_user = await user_repository.save_user(user)
    assert test_user is not None


@pytest.mark.asyncio
async def test_select_user_by_email_success(user_repository: SQLAlchemyUserRepository, create_test_user):
    user = LoginUserRequest(
        login="test_fixture_user@test.test",
        password="test_user_password"
    )
    test_user = await user_repository.select_user(user)
    assert test_user is not None


@pytest.mark.asyncio
async def test_select_user_by_username_success(user_repository: SQLAlchemyUserRepository, create_test_user):
    user = LoginUserRequest(
        login="test_fixture_user",
        password="test_user_password"
    )
    test_user = await user_repository.select_user(user)
    assert test_user is not None


@pytest.mark.asyncio
async def test_select_user_by_phone_number_success(user_repository: SQLAlchemyUserRepository, create_test_user):
    user = LoginUserRequest(
        login="+375112222222",
        password="test_user_password"
    )
    test_user = await user_repository.select_user(user)
    assert test_user is not None


@pytest.mark.asyncio
async def test_update_user_success(user_repository: SQLAlchemyUserRepository, create_test_user):
    test_user = await user_repository.update_user(create_test_user, "is_verified", True)
    assert test_user is not None


@pytest.mark.asyncio
async def test_duplicate_user_registration(user_repository: SQLAlchemyUserRepository, create_test_user):
    user = User(
        user_id=uuid.uuid4(),
        username="test_fixture_user",
        email="test_fixture_user@test.test",
        password="test_fixture_user_password",
        phone_number="+375112222222"
    )
    with pytest.raises(DuplicatedEntryError):
        await user_repository.save_user(user)


@pytest.mark.asyncio
async def test_select_user_with_invalid_login(user_repository: SQLAlchemyUserRepository, create_test_user):
    user = LoginUserRequest(
        login="invalid_user_login",
        password="test_user_password"
    )
    with pytest.raises(UserNotFoundException):
        await user_repository.select_user(user)
