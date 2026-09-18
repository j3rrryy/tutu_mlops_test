from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from dto import PredictionDTO

from ..mocks import FLOAT_VALUE, ID, MODEL_VERSION


@pytest.mark.asyncio
async def test_create_prediction(session, prediction_repository):
    dto = PredictionDTO(ID, FLOAT_VALUE + 1, MODEL_VERSION)

    res = await prediction_repository.create_prediction(dto)

    assert res == dto
    session.add.assert_called_once()


@pytest.mark.asyncio
async def test_create_prediction_exists(session, prediction, prediction_repository):
    dto = PredictionDTO(ID, FLOAT_VALUE + 1, MODEL_VERSION)
    session.add.side_effect = IntegrityError("", None, Exception(""))
    session.scalar = AsyncMock(return_value=prediction)

    res = await prediction_repository.create_prediction(dto)

    assert res == PredictionDTO(ID, FLOAT_VALUE, MODEL_VERSION)
    session.add.assert_called_once()


@pytest.mark.asyncio
async def test_create_prediction_concurrent_delete(session, prediction_repository):
    dto = PredictionDTO(ID, FLOAT_VALUE + 1, MODEL_VERSION)
    session.add.side_effect = IntegrityError("", None, Exception(""))
    prediction_repository.get_prediction = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await prediction_repository.create_prediction(dto)

    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert (
        exc_info.value.detail
        == f"Internal database error: Prediction {ID} vanished during upsert"
    )
    session.add.assert_called_once()


@pytest.mark.asyncio
async def test_create_prediction_exception(session, prediction_repository):
    dto = PredictionDTO(ID, FLOAT_VALUE, MODEL_VERSION)
    session.add.side_effect = SQLAlchemyError("Details")

    with pytest.raises(HTTPException) as exc_info:
        await prediction_repository.create_prediction(dto)

    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exc_info.value.detail == "Internal database error: Details"
    session.add.assert_called_once()


@pytest.mark.asyncio
async def test_get_prediction(session, prediction, prediction_repository):
    session.scalar = AsyncMock(return_value=prediction)

    res = await prediction_repository.get_prediction(ID)

    assert res == PredictionDTO(ID, FLOAT_VALUE, MODEL_VERSION)
    session.scalar.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_prediction_not_found(session, prediction_repository):
    session.scalar = AsyncMock(return_value=None)

    res = await prediction_repository.get_prediction(ID)

    assert res is None
    session.scalar.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_prediction_exception(session, prediction_repository):
    session.scalar.side_effect = SQLAlchemyError("Details")

    with pytest.raises(HTTPException) as exc_info:
        await prediction_repository.get_prediction(ID)

    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exc_info.value.detail == "Internal database error: Details"
    session.scalar.assert_awaited_once()
