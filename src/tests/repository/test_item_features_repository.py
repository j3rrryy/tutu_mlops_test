from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from dto import ItemFeaturesDTO

from ..mocks import FLOAT_VALUE, ITEM_ID, TIMESTAMP


@pytest.mark.asyncio
async def test_upsert_items(session, item_features_repository):
    dto = ItemFeaturesDTO(ITEM_ID, FLOAT_VALUE, FLOAT_VALUE, TIMESTAMP)

    res = await item_features_repository.upsert_items([dto])

    assert res is None
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_upsert_items_no_items(session, item_features_repository):
    res = await item_features_repository.upsert_items([])

    assert res is None
    session.execute.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_item_features(session, item_features, item_features_repository):
    session.scalar = AsyncMock(return_value=item_features)

    res = await item_features_repository.get_item_features(ITEM_ID)

    assert res == ItemFeaturesDTO(ITEM_ID, FLOAT_VALUE, FLOAT_VALUE, TIMESTAMP)
    session.scalar.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_item_features_not_found(session, item_features_repository):
    session.scalar = AsyncMock(return_value=None)

    res = await item_features_repository.get_item_features(ITEM_ID)

    assert res is None
    session.scalar.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_item_features_exception(session, item_features_repository):
    session.scalar.side_effect = SQLAlchemyError("Details")

    with pytest.raises(HTTPException) as exc_info:
        await item_features_repository.get_item_features(ITEM_ID)

    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exc_info.value.detail == "Internal database error: Details"
    session.scalar.assert_awaited_once()
