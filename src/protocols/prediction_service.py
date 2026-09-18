from typing import Protocol
from uuid import UUID

from dto import PredictionDTO, PredictionRequestDTO


class PredictionServiceProtocol(Protocol):
    async def create_prediction(
        self, prediction_request: PredictionRequestDTO
    ) -> PredictionDTO: ...

    async def get_prediction(self, request_id: UUID) -> PredictionDTO: ...
