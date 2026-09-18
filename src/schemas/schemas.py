from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from enums import Prepayment


class PredictionRequest(BaseModel):
    request_id: UUID
    item_id: str = Field(..., min_length=1)
    item_price: float = Field(..., ge=0)
    delivery_days: int = Field(..., ge=0)
    client_is_app: bool
    type_prepayment: Prepayment


class PredictionResponse(BaseModel):
    request_id: UUID
    prediction: float
    model_version: str

    model_config = ConfigDict(from_attributes=True)
