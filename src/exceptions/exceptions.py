from uuid import UUID

from fastapi import HTTPException, status


class DatabaseException(HTTPException):
    def __init__(self, exc: Exception):
        super().__init__(
            status.HTTP_500_INTERNAL_SERVER_ERROR, f"Internal database error: {exc}"
        )


class PredictionNotFoundError(HTTPException):
    def __init__(self, request_id: UUID):
        super().__init__(
            status.HTTP_404_NOT_FOUND, f"Prediction {request_id} not found"
        )


class ItemFeaturesNotFoundError(HTTPException):
    def __init__(self, item_id: str):
        super().__init__(
            status.HTTP_404_NOT_FOUND, f"Item {item_id} features not found"
        )
