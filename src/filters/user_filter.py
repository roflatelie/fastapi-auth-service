from enum import Enum
from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from src.adapters.orm_engines.models import User


class RoleType(str, Enum):
    Admin = "Admin"
    User = "User"


class UserFilter(Filter):
    username__in: Optional[list[str]] = Field(alias="username")
    role__neq: Optional[list[RoleType]] = Field(alias="roles")

    class Constants(Filter.Constants):
        model = User

    class Config:
        allow_population_by_field_name = True
