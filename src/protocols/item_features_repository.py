from typing import Protocol

from dto import ItemFeaturesDTO


class ItemFeaturesRepositoryProtocol(Protocol):
    async def upsert_items(self, items: list[ItemFeaturesDTO]) -> None: ...

    async def get_item_features(self, item_id: str) -> ItemFeaturesDTO | None: ...
