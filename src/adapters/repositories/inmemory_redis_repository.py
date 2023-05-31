from typing import Any


class InMemoryRedisRepository:
    def __init__(self):
        self.cache = {}

    async def add_cache(self, key: str, value: Any, expire: int = None) -> None:
        self.cache[key] = value

    async def get_value(self, key: str) -> dict:
        for cache in self.cache.values():
            if cache == key:
                return key
