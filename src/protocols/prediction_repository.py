from typing import Protocol
from uuid import UUID

from dto import PredictionDTO


class PredictionRepositoryProtocol(Protocol):
    async def create_prediction(self, prediction: PredictionDTO) -> PredictionDTO: ...

    async def get_prediction(self, request_id: UUID) -> PredictionDTO | None: ...
