from collections.abc import AsyncIterator

import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from main import main
from repository.models import Base


@pytest_asyncio.fixture(scope="session")
async def app() -> AsyncIterator[FastAPI]:
    application = main()
    async with application.router.lifespan_context(application):
        yield application


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    engine = app.state.engine
    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
