from datetime import UTC, datetime

import pytest
from fastapi import status

from dto import ItemFeaturesDTO
from repository import ItemFeaturesRepository

from ..mocks import ID, ITEM_ID

pytestmark = pytest.mark.e2e


async def test_predictions_full_scenario(app, client):
    repo = ItemFeaturesRepository(app.state.sessionmaker)
    await repo.upsert_items(
        [
            ItemFeaturesDTO(
                ITEM_ID, 0.773956, 623.1971, datetime(2026, 3, 21, 2, 0, 0, tzinfo=UTC)
            )
        ]
    )

    request_body = {
        "request_id": str(ID),
        "item_id": ITEM_ID,
        "item_price": 2500.0,
        "delivery_days": 4,
        "client_is_app": True,
        "type_prepayment": "card",
    }
    response_body = {
        "request_id": str(ID),
        "prediction": 501.34,
        "model_version": app.state.model_metadata["model_version"],
    }

    response = await client.post("/predictions", json=request_body)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == response_body

    repeat = await client.post("/predictions", json=request_body)
    assert repeat.status_code == status.HTTP_200_OK
    assert repeat.json() == response_body

    fetched = await client.get(f"/predictions/{ID}")
    assert fetched.status_code == status.HTTP_200_OK
    assert fetched.json() == response_body

    missing = await client.get("/predictions/00000000-0000-0000-0000-000000000000")
    assert missing.status_code == status.HTTP_404_NOT_FOUND

    request_body["request_id"] = "11111111-1111-1111-1111-111111111111"
    request_body["item_id"] = "MISSING"
    item_not_found = await client.post("/predictions", json=request_body)
    assert item_not_found.status_code == status.HTTP_404_NOT_FOUND
