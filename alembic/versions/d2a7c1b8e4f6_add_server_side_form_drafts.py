"""add server side form drafts

Revision ID: d2a7c1b8e4f6
Revises: c41a13f4d2b0
Create Date: 2026-03-19 00:00:02.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "d2a7c1b8e4f6"
down_revision: Union[str, None] = "c41a13f4d2b0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "form_drafts",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("draft_key", sa.String(length=512), nullable=False),
        sa.Column("path", sa.String(length=512), nullable=True),
        sa.Column("form_action", sa.String(length=512), nullable=True),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "tenant_id",
            "user_id",
            "draft_key",
            name="uq_form_drafts_tenant_user_key",
        ),
    )


def downgrade() -> None:
    op.drop_table("form_drafts")
