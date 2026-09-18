from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dto import PredictionDTO
from protocols import PredictionRepositoryProtocol
from utils import database_exception_handler

from .models import Prediction


class PredictionRepository(PredictionRepositoryProtocol):
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        self._sessionmaker = sessionmaker

    @database_exception_handler
    async def create_prediction(self, prediction: PredictionDTO) -> PredictionDTO:
        new_prediction = Prediction(
            request_id=prediction.request_id,
            prediction=prediction.prediction,
            model_version=prediction.model_version,
        )
        try:
            async with self._sessionmaker.begin() as session:
                session.add(new_prediction)
        except IntegrityError:
            existing = await self.get_prediction(prediction.request_id)
            if existing is None:
                raise SQLAlchemyError(
                    f"Prediction {prediction.request_id} vanished during upsert"
                )
            return existing
        return prediction

    @database_exception_handler
    async def get_prediction(self, request_id: UUID) -> PredictionDTO | None:
        async with self._sessionmaker() as session:
            prediction = await session.scalar(
                select(Prediction).where(Prediction.request_id == request_id)
            )
        if prediction is None:
            return None
        return PredictionDTO(
            prediction.request_id, prediction.prediction, prediction.model_version
        )
