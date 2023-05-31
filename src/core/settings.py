import os
from enum import Enum
from typing import Any

from pydantic import BaseSettings, Field, SecretStr


source_email: str = os.environ.get("HOST_EMAIL")


class EnvironmentTypes(Enum):
    test: str = "test"
    local: str = "local"
    dev: str = "dev"
    prod: str = "prod"


class BaseAppSettings(BaseSettings):
    environment: EnvironmentTypes = EnvironmentTypes.prod
    debug: bool = True
    title: str = "User Authentication service"
    allowed_hosts: list[str] = ["*"]
    db_driver_name: str = "postgresql+asyncpg"
    db_host: str = "auth-pg"
    db_username: str
    db_password: SecretStr
    db_database: str
    db_port: int | None
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str
    redis_host: str = "redis"
    redis_db: int = 0
    redis_post: int = 6379
    redis_pass: str
    secret_key: str

    @property
    def get_db_creds(self):
        return {
            "drivername": self.db_driver_name,
            "username": self.db_username,
            "host": self.db_host,
            "port": self.db_port,
            "database": self.db_database,
            "password": self.db_password.get_secret_value(),
        }

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            "debug": self.debug,
            "title": self.title,
        }

    @property
    def get_aws_creds(self):
        return {
            "aws_access_key_id": self.aws_access_key_id,
            "aws_secret_access_key": self.aws_secret_access_key,
            "region_name": self.region_name
        }

    @property
    def get_redis_creds(self):
        return {
            "host": self.redis_host,
            "port": self.redis_post,
            "db": self.redis_db,
            "password": self.redis_pass,
        }

    @property
    def get_secret_key(self):
        return self.secret_key


class TestSettings(BaseAppSettings):
    title: str = "Test environment"


class LocalSettings(BaseAppSettings):
    title: str = "Local environment"


class DevelopmentSettings(BaseAppSettings):
    title: str = "Development environment"


class ProductionSettings(BaseAppSettings):
    debug: bool = False
