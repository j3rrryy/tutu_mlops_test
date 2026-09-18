from typing import Annotated, Any

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from protocols import (
    ItemFeaturesRepositoryProtocol,
    PredictionModelProtocol,
    PredictionRepositoryProtocol,
    PredictionServiceProtocol,
)
from repository import ItemFeaturesRepository, PredictionRepository
from service import PredictionService


def get_sessionmaker(request: Request) -> async_sessionmaker[AsyncSession]:
    return request.app.state.sessionmaker


def get_prediction_model(request: Request) -> PredictionModelProtocol:
    return request.app.state.model


def get_prediction_model_metadata(request: Request) -> dict[str, Any]:
    return request.app.state.model_metadata


def get_prediction_repository(
    sessionmaker: Annotated[
        async_sessionmaker[AsyncSession], Depends(get_sessionmaker)
    ],
) -> PredictionRepositoryProtocol:
    return PredictionRepository(sessionmaker)


def get_item_features_repository(
    sessionmaker: Annotated[
        async_sessionmaker[AsyncSession], Depends(get_sessionmaker)
    ],
) -> ItemFeaturesRepositoryProtocol:
    return ItemFeaturesRepository(sessionmaker)


def get_prediction_service(
    prediction_model: Annotated[PredictionModelProtocol, Depends(get_prediction_model)],
    prediction_model_metadata: Annotated[
        dict[str, Any], Depends(get_prediction_model_metadata)
    ],
    prediction_repository: Annotated[
        PredictionRepositoryProtocol, Depends(get_prediction_repository)
    ],
    item_features_repository: Annotated[
        ItemFeaturesRepositoryProtocol, Depends(get_item_features_repository)
    ],
) -> PredictionServiceProtocol:
    return PredictionService(
        prediction_model,
        prediction_model_metadata,
        prediction_repository,
        item_features_repository,
    )


PredictionServiceDep = Annotated[
    PredictionServiceProtocol, Depends(get_prediction_service)
]
