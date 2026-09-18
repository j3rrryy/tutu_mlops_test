from typing import Protocol


class ItemFeaturesLoaderProtocol(Protocol):
    async def load_from_csv(self, csv_path: str) -> None: ...
