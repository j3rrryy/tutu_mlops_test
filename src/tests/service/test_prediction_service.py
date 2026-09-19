from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException, status

from dto import PredictionDTO, PredictionRequestDTO
from enums import Prepayment

from ..mocks import FLOAT_VALUE, ID, INT_VALUE, ITEM_ID, MODEL_VERSION


@pytest.mark.asyncio
async def test_create_prediction(
    mocked_prediction_repository,
    prediction_service,
    prediction_model,
    prediction_model_metadata,
):
    dto = PredictionRequestDTO(
        ID, ITEM_ID, FLOAT_VALUE, INT_VALUE, True, Prepayment.SBP
    )
    mocked_prediction_repository.get_prediction = AsyncMock(return_value=None)

    res = await prediction_service.create_prediction(dto)

    assert res == PredictionDTO(ID, FLOAT_VALUE, MODEL_VERSION)
    prediction_model.predict.assert_called_once()
    df = prediction_model.predict.call_args[0][0]
    assert list(df.columns) == prediction_model_metadata["features"]
    assert df["type_prepayment"].iloc[0] == "sbp"


@pytest.mark.asyncio
async def test_create_prediction_exists(prediction_service, prediction_model):
    dto = PredictionRequestDTO(
        ID, ITEM_ID, FLOAT_VALUE, INT_VALUE, True, Prepayment.SBP
    )

    res = await prediction_service.create_prediction(dto)

    assert res == PredictionDTO(ID, FLOAT_VALUE, MODEL_VERSION)
    prediction_model.predict.assert_not_called()


@pytest.mark.asyncio
async def test_create_prediction_item_features_not_found(
    mocked_prediction_repository,
    mocked_item_features_repository,
    prediction_service,
    prediction_model,
):
    dto = PredictionRequestDTO(
        ID, ITEM_ID, FLOAT_VALUE, INT_VALUE, True, Prepayment.SBP
    )
    mocked_prediction_repository.get_prediction = AsyncMock(return_value=None)
    mocked_item_features_repository.get_item_features = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await prediction_service.create_prediction(dto)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == f"Item {ITEM_ID} features not found"
    prediction_model.predict.assert_not_called()


@pytest.mark.asyncio
async def test_get_prediction(prediction_service):
    res = await prediction_service.get_prediction(ID)

    assert res == PredictionDTO(ID, FLOAT_VALUE, MODEL_VERSION)


@pytest.mark.asyncio
async def test_get_prediction_not_found(
    mocked_prediction_repository, prediction_service
):
    mocked_prediction_repository.get_prediction = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await prediction_service.get_prediction(ID)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == f"Prediction {ID} not found"
