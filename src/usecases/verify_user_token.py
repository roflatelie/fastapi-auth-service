from jose import jwt, JWTError

from src.adapters.repositories.redis_repository import RedisRepository
from src.core.config import settings
from src.core.exceptions import CredentialsValidationException, InvalidTokenException, InvalidPermissionsException
from src.domain.token import Token


class VerifyUserTokenUsecase:
    def __init__(self, redis_repository: RedisRepository):
        self.redis_repository = redis_repository

    async def verify_user_token(self, token: str) -> Token:
        try:
            if await self.redis_repository.get_value(token):
                raise CredentialsValidationException
            payload = jwt.decode(token, key=settings.get_secret_key)
            if payload is None:
                raise CredentialsValidationException
            token_data = Token(
                user_id=payload.get("user_id"),
                username=payload.get("username"),
                email=payload.get("email"),
                role=payload.get("role")
            )
            return token_data
        except JWTError as e:
            raise InvalidTokenException

    async def verify_admin_token(self, token: str) -> Token:
        user = await self.verify_user_token(token)
        if "Admin" not in user.role:
            raise InvalidPermissionsException

