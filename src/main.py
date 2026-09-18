import json
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import joblib  # type: ignore[import-untyped]
import uvicorn
from fastapi import FastAPI

from repository import create_engine_and_sessionmaker
from routers import prediction_router
from settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    engine, sessionmaker = create_engine_and_sessionmaker()
    app.state.engine = engine
    app.state.sessionmaker = sessionmaker
    app.state.model = joblib.load(Settings.MODEL_PATH)
    with open(Settings.MODEL_METADATA_PATH) as f:  # noqa: ASYNC230 - startup
        app.state.model_metadata = json.load(f)
    try:
        yield
    finally:
        await engine.dispose()


def main():
    app = FastAPI(
        title=Settings.APP_NAME,
        version=Settings.VERSION,
        debug=Settings.DEBUG,
        lifespan=lifespan,
    )
    app.include_router(prediction_router)
    return app


if __name__ == "__main__":
    uvicorn.run(
        "main:main",
        factory=True,
        loop="uvloop",
        host=Settings.HOST,
        port=Settings.PORT,
        workers=Settings.WORKERS,
        limit_max_requests=Settings.LIMIT_MAX_REQUESTS,
        reload=Settings.DEBUG,
    )
