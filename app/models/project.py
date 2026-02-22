import uuid
from enum import Enum
from sqlalchemy import String, Text, Enum as SQLEnum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel, TimestampMixin


class ProjectStatus(str, Enum):
    """Project status enumeration."""

    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class ResponseStatus(str, Enum):
    """Response status for controls."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"


class Project(BaseModel, TimestampMixin):
    """Assessment/audit project model."""

    __tablename__ = "projects"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenants.id"), nullable=False
    )
    client_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("clients.id"), nullable=False
    )
    framework_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("frameworks.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[ProjectStatus] = mapped_column(
        SQLEnum(ProjectStatus), nullable=False, default=ProjectStatus.DRAFT
    )

    # Relationships
    client: Mapped["Client"] = relationship()
    framework: Mapped["Framework"] = relationship()


class ProjectMember(BaseModel, TimestampMixin):
    """Team member assignment to a project."""

    __tablename__ = "project_members"

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    role: Mapped[str] = mapped_column(String(50), nullable=False)


class ProjectResponse(BaseModel, TimestampMixin):
    """Response to a framework control within a project."""

    __tablename__ = "project_responses"

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id"), nullable=False
    )
    framework_control_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("framework_controls.id"), nullable=False
    )
    response_text: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[ResponseStatus] = mapped_column(
        SQLEnum(ResponseStatus), nullable=False, default=ResponseStatus.NOT_STARTED
    )
    assigned_to_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )


class ProjectEvidenceFile(BaseModel, TimestampMixin):
    """Evidence file attachment for a project response."""

    __tablename__ = "project_evidence_files"

    project_response_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("project_responses.id"), nullable=False
    )
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=True)
    file_type: Mapped[str] = mapped_column(String(50), nullable=True)
