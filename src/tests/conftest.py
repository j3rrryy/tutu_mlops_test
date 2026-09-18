from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dependencies import get_prediction_service
from main import main
from protocols import (
    ItemFeaturesLoaderProtocol,
    ItemFeaturesRepositoryProtocol,
    PredictionModelProtocol,
    PredictionRepositoryProtocol,
    PredictionServiceProtocol,
)
from repository import (
    ItemFeatures,
    ItemFeaturesRepository,
    Prediction,
    PredictionRepository,
)
from service import ItemFeaturesLoader, PredictionService

from .mocks import (
    create_empty_mock_csv,
    create_item_features,
    create_item_features_repository,
    create_mock_csv,
    create_prediction,
    create_prediction_model,
    create_prediction_model_metadata,
    create_prediction_repository,
    create_session,
    create_sessionmaker,
)


@pytest.fixture
def session() -> AsyncSession:
    return create_session()


@pytest.fixture
def sessionmaker(session) -> async_sessionmaker[AsyncSession]:
    return create_sessionmaker(session)


@pytest.fixture
def prediction_repository(sessionmaker) -> PredictionRepositoryProtocol:
    return PredictionRepository(sessionmaker)


@pytest.fixture
def item_features_repository(sessionmaker) -> ItemFeaturesRepositoryProtocol:
    return ItemFeaturesRepository(sessionmaker)


@pytest.fixture
def mocked_prediction_repository() -> PredictionRepositoryProtocol:
    return create_prediction_repository()


@pytest.fixture
def mocked_item_features_repository() -> ItemFeaturesRepositoryProtocol:
    return create_item_features_repository()


@pytest.fixture
def prediction_model() -> PredictionModelProtocol:
    return create_prediction_model()


@pytest.fixture
def prediction_model_metadata() -> dict[str, Any]:
    return create_prediction_model_metadata()


@pytest.fixture
def prediction_service(
    prediction_model,
    prediction_model_metadata,
    mocked_prediction_repository,
    mocked_item_features_repository,
) -> PredictionServiceProtocol:
    return PredictionService(
        prediction_model,
        prediction_model_metadata,
        mocked_prediction_repository,
        mocked_item_features_repository,
    )


@pytest.fixture
def item_features_loader(mocked_item_features_repository) -> ItemFeaturesLoaderProtocol:
    return ItemFeaturesLoader(mocked_item_features_repository)


@pytest.fixture
def mock_csv(tmp_path) -> str:
    return create_mock_csv(tmp_path)


@pytest.fixture
def empty_mock_csv(tmp_path) -> str:
    return create_empty_mock_csv(tmp_path)


@pytest.fixture
def client(prediction_service) -> TestClient:
    app = main()
    app.dependency_overrides[get_prediction_service] = lambda: prediction_service
    return TestClient(app)


@pytest.fixture
def prediction() -> Prediction:
    return create_prediction()


@pytest.fixture
def item_features() -> ItemFeatures:
    return create_item_features()
