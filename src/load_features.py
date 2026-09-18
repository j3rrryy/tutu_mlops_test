import uvloop

from repository import ItemFeaturesRepository, create_engine_and_sessionmaker
from service import ItemFeaturesLoader
from settings import Settings


async def main() -> None:
    engine, sessionmaker = create_engine_and_sessionmaker()
    try:
        repository = ItemFeaturesRepository(sessionmaker)
        loader = ItemFeaturesLoader(repository)
        await loader.load_from_csv(Settings.FEATURES_PATH)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    uvloop.run(main())
