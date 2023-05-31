from pydantic import BaseModel

from src.domain.user import User


class CreateUserRequest(BaseModel):
    username: str
    email: str
    phone_number: str
    password: str

    def to_entity(self):
        return User(
            username=self.username,
            email=self.email,
            password=self.password,
            phone_number=self.phone_number
        )


class CreateUserResponse(BaseModel):
    detail: str


class LoginUserRequest(BaseModel):
    login: str
    password: str


class TokenResponse(BaseModel):
    access_token: str


class ResetUserPasswordRequest(BaseModel):
    password: str


class GetUserRequest(BaseModel):
    user_id: str
