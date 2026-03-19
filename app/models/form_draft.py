import uuid
from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel, TimestampMixin


class FormDraft(BaseModel, TimestampMixin):
    """Server-side draft snapshot for a single user's form."""

    __tablename__ = "form_drafts"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "user_id",
            "draft_key",
            name="uq_form_drafts_tenant_user_key",
        ),
    )

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenants.id"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    draft_key: Mapped[str] = mapped_column(String(512), nullable=False)
    path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    form_action: Mapped[str | None] = mapped_column(String(512), nullable=True)
    payload_json: Mapped[str] = mapped_column(Text, nullable=False)
