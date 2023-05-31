from src.adapters.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository


class VerifyUserEmailUsecase:
    def __init__(self, user_repository: SQLAlchemyUserRepository):
        self.user_repository = user_repository

    async def update_email_verification(self, user_id: str) -> dict:
        msg = await self.user_repository.update_user(user_id, "is_verified", True)
        return msg
