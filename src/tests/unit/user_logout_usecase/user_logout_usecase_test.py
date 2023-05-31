import pytest

from src.adapters.repositories.inmemory_redis_repository import InMemoryRedisRepository
from src.core.exceptions import UserLogoutException
from src.usecases.user_logout import UserLogoutUsecase


@pytest.fixture
def redis_repository():
    return InMemoryRedisRepository()


@pytest.fixture
def user_logout_usecase(redis_repository):
    return UserLogoutUsecase(redis_repository)


@pytest.mark.asyncio
async def test_user_logout_success(user_logout_usecase, redis_repository):
    access_token = "access_token"
    refresh_token = "refresh_token"
    await user_logout_usecase.logout_user(access_token, refresh_token)
    assert redis_repository.cache.get(access_token) == 1
    assert redis_repository.cache.get(refresh_token) == 1


@pytest.mark.asyncio
async def test_user_logout_with_blacklisted_tokens(user_logout_usecase, redis_repository):
    access_token = "access_token"
    refresh_token = "refresh_token"
    await user_logout_usecase.logout_user(access_token, refresh_token)
    with pytest.raises(UserLogoutException):
        await user_logout_usecase.logout_user(access_token, refresh_token)
