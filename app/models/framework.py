import uuid
from sqlalchemy import String, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel, TimestampMixin


class Framework(BaseModel, TimestampMixin):
    """Compliance framework model (e.g., ISO 27001, SOC 2)."""

    __tablename__ = "frameworks"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenants.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    version: Mapped[str] = mapped_column(String(50), nullable=True)

    # Relationships
    sections: Mapped[list["FrameworkSection"]] = relationship(
        back_populates="framework", cascade="all, delete-orphan"
    )


class FrameworkSection(BaseModel, TimestampMixin):
    """Section/domain within a framework (e.g., Access Control)."""

    __tablename__ = "framework_sections"

    framework_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("frameworks.id"), nullable=False
    )
    parent_section_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("framework_sections.id"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    framework: Mapped["Framework"] = relationship(back_populates="sections")
    controls: Mapped[list["FrameworkControl"]] = relationship(
        back_populates="section", cascade="all, delete-orphan"
    )


class FrameworkControl(BaseModel, TimestampMixin):
    """Individual control within a framework section."""

    __tablename__ = "framework_controls"

    framework_section_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("framework_sections.id"), nullable=False
    )
    control_id: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    implementation_guidance: Mapped[str] = mapped_column(Text, nullable=True)

    # Relationships
    section: Mapped["FrameworkSection"] = relationship(back_populates="controls")


class ChecklistItem(BaseModel, TimestampMixin):
    """Checklist item associated with a control."""

    __tablename__ = "checklist_items"

    framework_control_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("framework_controls.id"), nullable=False
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_mandatory: Mapped[bool] = mapped_column(default=True)
