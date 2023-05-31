from src.adapters.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.domain.user import User


class UserSignUpUsecase:
    def __init__(self, user_repository: SQLAlchemyUserRepository):
        self.user_repository = user_repository

    async def register_user(self, user: User) -> User:
        user = await self.user_repository.save_user(user)
        return user
