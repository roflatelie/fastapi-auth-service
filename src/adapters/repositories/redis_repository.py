import json
from typing import Any

from redis import asyncio as aioredis

from src.core.config import settings
from src.core.exceptions import RequestProcessingException


class RedisRepository:
    def __init__(self):
        redis_creds = settings.get_redis_creds
        self.redis_connection = aioredis.Redis(**redis_creds)

    async def add_cache(self, key: str, value: Any, expire: int = None) -> None:
        try:
            json_value = json.dumps(value)
            if expire is None:
                await self.redis_connection.set(key, json_value)
            else:
                await self.redis_connection.setex(key, expire, json_value)
        except aioredis.RedisError:
            raise RequestProcessingException

    async def get_value(self, key: str) -> dict:
        try:
            json_value = await self.redis_connection.get(key)
            if json_value is not None:
                return json.loads(json_value)
        except aioredis.RedisError:
            raise RequestProcessingException
