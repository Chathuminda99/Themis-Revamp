import uuid
from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel, TimestampMixin


class Tenant(BaseModel, TimestampMixin):
    """Organization/tenant model."""

    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    logo_url: Mapped[str] = mapped_column(String(512), nullable=True)
    settings: Mapped[dict] = mapped_column(JSON, nullable=True, default={})
