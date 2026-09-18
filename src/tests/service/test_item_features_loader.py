from datetime import UTC, datetime

import pytest


@pytest.mark.asyncio
async def test_load_from_csv_loads_valid_rows(
    mock_csv, item_features_loader, mocked_item_features_repository
):
    await item_features_loader.load_from_csv(mock_csv)

    items = mocked_item_features_repository.upsert_items.call_args[0][0]
    assert {it.item_id for it in items} == {"ITEM-001", "ITEM-002"}
    mocked_item_features_repository.upsert_items.assert_awaited_once()


@pytest.mark.asyncio
async def test_load_from_csv_skips_invalid_rows(
    mock_csv, item_features_loader, mocked_item_features_repository
):
    await item_features_loader.load_from_csv(mock_csv)

    items = mocked_item_features_repository.upsert_items.call_args[0][0]
    assert "ITEM-003" not in {it.item_id for it in items}


@pytest.mark.asyncio
async def test_load_from_csv_last_duplicate_wins(
    mock_csv, item_features_loader, mocked_item_features_repository
):
    await item_features_loader.load_from_csv(mock_csv)

    items = mocked_item_features_repository.upsert_items.call_args[0][0]
    item_001 = next(it for it in items if it.item_id == "ITEM-001")
    assert item_001.historical_return_rate == 0.7
    assert item_001.avg_item_losses_30d == 150.0
    assert item_001.updated_at == datetime(2026, 1, 3, tzinfo=UTC)


@pytest.mark.asyncio
async def test_load_from_csv_no_rows(
    empty_mock_csv, item_features_loader, mocked_item_features_repository
):
    await item_features_loader.load_from_csv(empty_mock_csv)

    mocked_item_features_repository.upsert_items.assert_not_awaited()
