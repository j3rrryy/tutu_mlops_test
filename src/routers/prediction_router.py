from uuid import UUID

from fastapi import APIRouter, status

from dependencies import PredictionServiceDep
from dto import PredictionRequestDTO
from schemas import PredictionRequest, PredictionResponse

prediction_router = APIRouter(prefix="/predictions", tags=["predictions"])


@prediction_router.post(
    "", response_model=PredictionResponse, status_code=status.HTTP_200_OK
)
async def create_prediction(
    prediction_request: PredictionRequest, prediction_service: PredictionServiceDep
) -> PredictionResponse:
    dto = PredictionRequestDTO(
        prediction_request.request_id,
        prediction_request.item_id,
        prediction_request.item_price,
        prediction_request.delivery_days,
        prediction_request.client_is_app,
        prediction_request.type_prepayment,
    )
    prediction = await prediction_service.create_prediction(dto)
    return PredictionResponse.model_validate(prediction)


@prediction_router.get(
    "/{request_id}", response_model=PredictionResponse, status_code=status.HTTP_200_OK
)
async def get_prediction(
    request_id: UUID, prediction_service: PredictionServiceDep
) -> PredictionResponse:
    prediction = await prediction_service.get_prediction(request_id)
    return PredictionResponse.model_validate(prediction)
