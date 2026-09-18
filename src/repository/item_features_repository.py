from dataclasses import asdict

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dto import ItemFeaturesDTO
from protocols import ItemFeaturesRepositoryProtocol
from utils import database_exception_handler

from .models import ItemFeatures


class ItemFeaturesRepository(ItemFeaturesRepositoryProtocol):
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        self._sessionmaker = sessionmaker

    async def upsert_items(self, items: list[ItemFeaturesDTO]) -> None:
        if not items:
            return
        values = [asdict(item) for item in items]
        stmt = pg_insert(ItemFeatures).values(values)
        stmt = stmt.on_conflict_do_update(
            index_elements=[ItemFeatures.item_id],
            set_={
                "historical_return_rate": stmt.excluded.historical_return_rate,
                "avg_item_losses_30d": stmt.excluded.avg_item_losses_30d,
                "updated_at": stmt.excluded.updated_at,
            },
        )
        async with self._sessionmaker.begin() as session:
            await session.execute(stmt)

    @database_exception_handler
    async def get_item_features(self, item_id: str) -> ItemFeaturesDTO | None:
        async with self._sessionmaker() as session:
            item_features = await session.scalar(
                select(ItemFeatures).where(ItemFeatures.item_id == item_id)
            )
        if item_features is None:
            return None
        return ItemFeaturesDTO(
            item_features.item_id,
            item_features.historical_return_rate,
            item_features.avg_item_losses_30d,
            item_features.updated_at,
        )
