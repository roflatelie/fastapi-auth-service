from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class SQLAlchemy:
    def __init__(self, session_maker):
        self.session_maker = session_maker

    @classmethod
    def start(cls, db_credentials: dict):
        database_url = URL.create(**db_credentials)
        engine = create_async_engine(database_url, echo=False)
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False, autoflush=False, autocommit=False
        )
        return cls(async_session)