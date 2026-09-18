from typing import Any
from uuid import UUID

import pandas as pd

from dto import ItemFeaturesDTO, PredictionDTO, PredictionRequestDTO
from exceptions import ItemFeaturesNotFoundError, PredictionNotFoundError
from protocols import (
    ItemFeaturesRepositoryProtocol,
    PredictionModelProtocol,
    PredictionRepositoryProtocol,
    PredictionServiceProtocol,
)


class PredictionService(PredictionServiceProtocol):
    def __init__(
        self,
        prediction_model: PredictionModelProtocol,
        prediction_model_metadata: dict[str, Any],
        prediction_repository: PredictionRepositoryProtocol,
        item_features_repository: ItemFeaturesRepositoryProtocol,
    ):
        self._prediction_model = prediction_model
        self._prediction_model_metadata = prediction_model_metadata
        self._prediction_repository = prediction_repository
        self._item_features_repository = item_features_repository

    async def create_prediction(
        self, prediction_request: PredictionRequestDTO
    ) -> PredictionDTO:
        existing = await self._prediction_repository.get_prediction(
            prediction_request.request_id
        )
        if existing is not None:
            return existing

        item = await self._item_features_repository.get_item_features(
            prediction_request.item_id
        )
        if item is None:
            raise ItemFeaturesNotFoundError(prediction_request.item_id)

        df = self._build_df(prediction_request, item)
        raw = self._prediction_model.predict(df)
        return await self._prediction_repository.create_prediction(
            PredictionDTO(
                prediction_request.request_id,
                round(float(raw[0]), 2),
                self._prediction_model_metadata["model_version"],
            )
        )

    async def get_prediction(self, request_id: UUID) -> PredictionDTO:
        prediction = await self._prediction_repository.get_prediction(request_id)
        if prediction is None:
            raise PredictionNotFoundError(request_id)
        return prediction

    def _build_df(
        self, prediction_request: PredictionRequestDTO, item_features: ItemFeaturesDTO
    ) -> pd.DataFrame:
        row = {
            "item_price": prediction_request.item_price,
            "delivery_days": prediction_request.delivery_days,
            "client_is_app": prediction_request.client_is_app,
            "type_prepayment": prediction_request.type_prepayment.value,
            "historical_return_rate": item_features.historical_return_rate,
            "avg_item_losses_30d": item_features.avg_item_losses_30d,
        }
        return pd.DataFrame([row], columns=self._prediction_model_metadata["features"])
