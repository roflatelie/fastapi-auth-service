import pytest
import asyncio


import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.adapters.orm_engines.models import Base
from src.core.config import settings
from src.main import app


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def engine():
    engine = create_async_engine(URL.create(**settings.get_db_creds))
    yield engine
    engine.sync_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def create(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def session(engine):
    async with AsyncSession(engine) as async_session:
        yield async_session


@pytest_asyncio.fixture
async def test_app(event_loop):
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8080 ") as ac:
        yield ac


@pytest_asyncio.fixture
async def create_test_user(test_app: AsyncClient):
    payload = {
        "username": "api_test_user",
        "email": "api_test_user@test.test",
        "phone_number": "+375331133256",
        "password": "api_test_user_password"
    }
    await test_app.post("/users/signup/", json=payload)

