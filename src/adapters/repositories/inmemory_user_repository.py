import uuid
from typing import Any

from src.ports.repositories.user_repository import UserRepository
from src.domain.user import User


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {}

    async def save_user(self, user: User) -> User:
        user.user_id = uuid.uuid4()
        self.users[user.user_id] = user
        return user

    async def select_user(self, user):
        for user_db in self.users.values():
            if user_db.username == user.login or user_db.email == user.login or user_db.phone_number == user.login:
                return user

    async def update_user(self, user_id: str, column_name: str, value: Any) -> dict:
        if user_id in self.users:
            return {"success": True}
        else:
            return {"success": False}
