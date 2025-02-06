from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.core.config import get_settings, Settings

settings: Settings = get_settings()


class Base(DeclarativeBase):
    ...


class DBManager:
    def __init__(self, base_model: type[DeclarativeBase], db_url: str, **kwargs) -> None:
        self.model_base = base_model
        self.db_url = db_url

        self.engine = create_async_engine(db_url, **kwargs)
        self.session_maker = async_sessionmaker(self.engine, expire_on_commit=False)

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.model_base.metadata.create_all)

    async def drop_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.model_base.metadata.drop_all)

    def get_session(self):
        return self.session_maker()

    def begin(self):
        return self.session_maker.begin()


SQL_DB = DBManager(
    base_model=Base,
    db_url=settings.database_url,
    echo=True
)


async def get_db():
    return SQL_DB