from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ItemFeatures(Base):
    __tablename__ = "item_features"

    item_id: Mapped[str] = mapped_column(sa.String(255), primary_key=True)
    historical_return_rate: Mapped[float] = mapped_column(sa.Float, nullable=False)
    avg_item_losses_30d: Mapped[float] = mapped_column(sa.Float, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP(timezone=True), nullable=False
    )


class Prediction(Base):
    __tablename__ = "predictions"

    request_id: Mapped[UUID] = mapped_column(PG_UUID(), primary_key=True)
    prediction: Mapped[float] = mapped_column(sa.Float, nullable=False)
    model_version: Mapped[str] = mapped_column(sa.String(50), nullable=False)
