from src.adapters.repositories.redis_repository import RedisRepository
from src.core.exceptions import UserLogoutException


class UserLogoutUsecase:
    def __init__(self, redis_repository: RedisRepository):
        self.redis_repository = redis_repository

    async def logout_user(self, access_token: str, refresh_token: str) -> None:
        try:
            await self.redis_repository.add_cache(key=access_token, value=1, expire=1800)
            await self.redis_repository.add_cache(key=refresh_token, value=1, expire=28800)
        except Exception as e:
            print(e)
            raise UserLogoutException
