from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.user import User


class UserRepository(ABC):

    @abstractmethod
    async def save_user(self, user: User) -> UUID:
        pass
