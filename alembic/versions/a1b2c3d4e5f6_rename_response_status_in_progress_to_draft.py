"""rename response_status in_progress to draft

Revision ID: a1b2c3d4e5f6
Revises: e0c18c7a7514
Create Date: 2026-03-19 12:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = 'd2a7c1b8e4f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    # Commit current transaction so ALTER TYPE ADD VALUE takes effect
    conn.execute(sa.text("COMMIT"))
    conn.execute(sa.text("ALTER TYPE responsestatus ADD VALUE IF NOT EXISTS 'DRAFT'"))
    # Begin a new transaction for the UPDATE
    conn.execute(sa.text("BEGIN"))
    conn.execute(
        sa.text(
            "UPDATE project_responses SET status = 'DRAFT'::responsestatus "
            "WHERE status::text = 'IN_PROGRESS'"
        )
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            "UPDATE project_responses SET status = 'IN_PROGRESS'::responsestatus "
            "WHERE status::text = 'DRAFT'"
        )
    )
