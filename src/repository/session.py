from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from settings import Settings


def create_engine_and_sessionmaker() -> tuple[
    AsyncEngine, async_sessionmaker[AsyncSession]
]:
    url = URL.create(
        Settings.POSTGRES_DRIVER,
        Settings.POSTGRES_USER,
        Settings.POSTGRES_PASSWORD,
        Settings.POSTGRES_HOST,
        Settings.POSTGRES_PORT,
        Settings.POSTGRES_DB,
    )
    engine = create_async_engine(
        url,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=15,
        pool_timeout=30,
        pool_recycle=1800,
    )
    sessionmaker = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    return engine, sessionmaker
