from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from enums import Prepayment


@dataclass(frozen=True, slots=True)
class ItemFeaturesDTO:
    item_id: str
    historical_return_rate: float
    avg_item_losses_30d: float
    updated_at: datetime


@dataclass(frozen=True, slots=True)
class PredictionRequestDTO:
    request_id: UUID
    item_id: str
    item_price: float
    delivery_days: int
    client_is_app: bool
    type_prepayment: Prepayment


@dataclass(frozen=True, slots=True)
class PredictionDTO:
    request_id: UUID
    prediction: float
    model_version: str
