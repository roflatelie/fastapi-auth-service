from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:
    user_id: UUID
    username: str
    email: str
    phone_number: str
    password: str
    role: list


@dataclass
class UserForAdmin:
    user_id: str
    username: str
    email: str
    phone_number: str
    role: list
