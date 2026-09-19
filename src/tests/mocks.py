from datetime import datetime
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dto import ItemFeaturesDTO, PredictionDTO
from protocols import (
    ItemFeaturesRepositoryProtocol,
    PredictionModelProtocol,
    PredictionRepositoryProtocol,
)
from repository import (
    ItemFeatures,
    ItemFeaturesRepository,
    Prediction,
    PredictionRepository,
)

ID = UUID("9e597dee-4253-4a30-8ec3-20a1cb10d56f")
ITEM_ID = "ITEM-001"
INT_VALUE = 3
FLOAT_VALUE = 0.75
MODEL_VERSION = "1.0.0"
TIMESTAMP = datetime.fromisoformat("1970-01-01T00:02:03Z")


def create_session() -> AsyncSession:
    return AsyncMock(spec=AsyncSession)


def create_sessionmaker(session) -> async_sessionmaker[AsyncSession]:
    sessionmaker = MagicMock(spec=async_sessionmaker[AsyncSession])
    sessionmaker.return_value.__aenter__.return_value = session
    sessionmaker.begin.return_value.__aenter__.return_value = session
    return sessionmaker


def create_prediction_repository() -> PredictionRepositoryProtocol:
    crud = AsyncMock(spec=PredictionRepository)
    prediction = PredictionDTO(ID, FLOAT_VALUE, MODEL_VERSION)
    crud.create_prediction = AsyncMock(return_value=prediction)
    crud.get_prediction = AsyncMock(return_value=prediction)
    return crud


def create_item_features_repository() -> ItemFeaturesRepositoryProtocol:
    crud = AsyncMock(spec=ItemFeaturesRepository)
    crud.upsert_items = AsyncMock(return_value=None)
    crud.get_item_features = AsyncMock(
        return_value=ItemFeaturesDTO(ITEM_ID, FLOAT_VALUE, FLOAT_VALUE, TIMESTAMP)
    )
    return crud


def create_prediction() -> Prediction:
    return Prediction(
        request_id=ID, prediction=FLOAT_VALUE, model_version=MODEL_VERSION
    )


def create_prediction_model() -> PredictionModelProtocol:
    model = MagicMock(spec=PredictionModelProtocol)
    model.predict = MagicMock(return_value=np.array([FLOAT_VALUE]))
    return model


def create_prediction_model_metadata() -> dict[str, Any]:
    return {
        "model_name": "item-loss-predictor",
        "model_version": MODEL_VERSION,
        "target": "item_losses",
        "features": [
            "item_price",
            "delivery_days",
            "client_is_app",
            "type_prepayment",
            "historical_return_rate",
            "avg_item_losses_30d",
        ],
        "feature_types": {
            "item_price": "float",
            "delivery_days": "integer",
            "client_is_app": "boolean",
            "type_prepayment": "string",
            "historical_return_rate": "float",
            "avg_item_losses_30d": "float",
        },
        "sklearn_version": "1.6.1",
        "created_at": TIMESTAMP.isoformat(),
    }


def create_mock_csv(tmp_path: Path) -> str:
    csv_file = tmp_path / "item_features.csv"
    csv_file.write_text(
        "item_id,historical_return_rate,avg_item_losses_30d,updated_at\n"
        "ITEM-001,0.5,100.0,2026-01-01T00:00:00Z\n"
        "ITEM-001,0.7,150.0,2026-01-03T00:00:00Z\n"
        "ITEM-002,0.3,200.0,2026-01-02T00:00:00Z\n"
        "ITEM-003,,300.0\n"
    )
    return str(csv_file)


def create_empty_mock_csv(tmp_path: Path) -> str:
    csv_file = tmp_path / "item_features.csv"
    csv_file.write_text(
        "item_id,historical_return_rate,avg_item_losses_30d,updated_at\n"
    )
    return str(csv_file)


def create_item_features() -> ItemFeatures:
    return ItemFeatures(
        item_id=ITEM_ID,
        historical_return_rate=FLOAT_VALUE,
        avg_item_losses_30d=FLOAT_VALUE,
        updated_at=TIMESTAMP,
    )
