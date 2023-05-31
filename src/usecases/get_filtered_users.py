from src.adapters.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.filters.user_filter import UserFilter


class FilterUsersUsecase:
    def __init__(self, user_repository: SQLAlchemyUserRepository):
        self.user_repository = user_repository

    async def get_filtered_users(self, user_filter: UserFilter):
        users = await self.user_repository.select_filtered_users(user_filter)
        return users
