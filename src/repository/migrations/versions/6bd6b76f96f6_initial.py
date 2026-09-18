"""initial

Revision ID: 6bd6b76f96f6
Revises:
Create Date: 2026-09-18 13:25:51.272640

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6bd6b76f96f6"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "item_features",
        sa.Column("item_id", sa.String(length=255), nullable=False),
        sa.Column("historical_return_rate", sa.Float(), nullable=False),
        sa.Column("avg_item_losses_30d", sa.Float(), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("item_id"),
    )
    op.create_table(
        "predictions",
        sa.Column("request_id", sa.UUID(), nullable=False),
        sa.Column("prediction", sa.Float(), nullable=False),
        sa.Column("model_version", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("request_id"),
    )


def downgrade() -> None:
    op.drop_table("predictions")
    op.drop_table("item_features")
