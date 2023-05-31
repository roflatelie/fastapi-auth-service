from src.adapters.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.usecases.password_hash import get_password_hash


class ResetPasswordUsecase:
    def __init__(self, user_repository: SQLAlchemyUserRepository):
        self.user_repository = user_repository

    async def update_password(self, password: str, user_id: str) -> dict:
        hash_password = get_password_hash(password)
        msg = await self.user_repository.update_user(user_id, "password", hash_password)
        return msg
