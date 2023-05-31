from uuid import UUID

from src.adapters.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from dataclasses import asdict


class SelectUserByUUIDUsecase:

    def __init__(self, user_repository: SQLAlchemyUserRepository):
        self.user_repository = user_repository

    async def login_user(self, user_id: UUID) -> dict:
        user = await self.user_repository.select_user_by_uuid(user_id)
        return asdict(user)
