from fastapi import status

from enums import Prepayment
from schemas import PredictionRequest, PredictionResponse

from ..mocks import FLOAT_VALUE, ID, INT_VALUE, MODEL_VERSION

PREFIX = "/predictions"


def test_create_prediction(client):
    data = PredictionRequest(
        request_id=ID,
        item_id=str(ID),
        item_price=FLOAT_VALUE,
        delivery_days=INT_VALUE,
        client_is_app=True,
        type_prepayment=Prepayment.SBP,
    )

    response = client.post(PREFIX, json=data.model_dump(mode="json"))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == PredictionResponse(
        request_id=ID, prediction=FLOAT_VALUE, model_version=MODEL_VERSION
    ).model_dump(mode="json")


def test_get_prediction(client):
    response = client.get(f"{PREFIX}/{ID}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == PredictionResponse(
        request_id=ID, prediction=FLOAT_VALUE, model_version=MODEL_VERSION
    ).model_dump(mode="json")
