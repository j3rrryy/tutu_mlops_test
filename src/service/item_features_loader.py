import csv
import logging
from datetime import datetime

from pydantic import BaseModel, Field, ValidationError

from dto import ItemFeaturesDTO
from protocols import ItemFeaturesLoaderProtocol, ItemFeaturesRepositoryProtocol

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ItemFeatureRow(BaseModel):
    item_id: str = Field(min_length=1)
    historical_return_rate: float = Field(ge=0, le=1)
    avg_item_losses_30d: float = Field(ge=0)
    updated_at: datetime


class ItemFeaturesLoader(ItemFeaturesLoaderProtocol):
    def __init__(self, item_features_repository: ItemFeaturesRepositoryProtocol):
        self._item_features_repository = item_features_repository

    async def load_from_csv(self, csv_path: str) -> None:
        rows_by_id: dict[str, ItemFeaturesDTO] = {}
        skipped = 0

        with open(csv_path, newline="", encoding="utf-8") as f:  # noqa: ASYNC230 - no other concurrent tasks in loader
            reader = csv.DictReader(f)
            for n, raw in enumerate(reader, start=2):
                try:
                    row = ItemFeatureRow.model_validate(raw)
                except ValidationError as exc:
                    skipped += 1
                    logger.warning("Skipping line #%d: %s", n, exc.errors()[0]["msg"])
                    continue

                rows_by_id[row.item_id] = ItemFeaturesDTO(
                    item_id=row.item_id,
                    historical_return_rate=row.historical_return_rate,
                    avg_item_losses_30d=row.avg_item_losses_30d,
                    updated_at=row.updated_at,
                )

        if items := list(rows_by_id.values()):
            await self._item_features_repository.upsert_items(items)

        logger.info("Loaded %d rows, skipped %d", len(items), skipped)
