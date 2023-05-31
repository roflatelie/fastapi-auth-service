from dataclasses import dataclass
from uuid import UUID


@dataclass
class Token:
    user_id: UUID
    username: str
    email: str
    role: list
