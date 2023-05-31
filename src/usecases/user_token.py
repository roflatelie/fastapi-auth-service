from datetime import timedelta, datetime
from jose import jwt

from src.adapters.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.core.exceptions import InvalidPasswordException
from src.domain.user import User
from src.usecases.password_hash import verify_password
from src.core.config import settings


class UserLoginUsecase:

    def __init__(self, user_repository: SQLAlchemyUserRepository):
        self.user_repository = user_repository

    async def login_user(self, user: User) -> dict:
        user_db = await self.user_repository.select_user(user)
        if verify_password(user.password, user_db.password):
            subject = {"id": str(user_db.user_id), "username": user_db.username,
                       "email": user_db.email, "role": user_db.role}
            print(user_db.role)
            access_token = self.generate_token(subject=subject, expire_time=30)
            refresh_token = self.generate_token(subject=subject, expire_time=480)
            return {"access_token": access_token,
                    "refresh_token": refresh_token}
        raise InvalidPasswordException

    @staticmethod
    def generate_token(subject: dict, expire_time: int) -> str:
        payload = {
            "user_id": subject.get("id"),
            "username": subject.get("username"),
            "email": subject.get("email"),
            "role": subject.get("role"),
            "exp": datetime.utcnow() + timedelta(minutes=expire_time),
        }
        token = jwt.encode(payload, key=settings.get_secret_key, algorithm="HS256")
        return token
