"""Workflow execution model for guided assessment workflows."""

import uuid
from enum import Enum
from sqlalchemy import String, Text, Enum as SQLEnum, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel, TimestampMixin


class WorkflowExecutionStatus(str, Enum):
    """Status of a workflow execution."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class WorkflowExecution(BaseModel, TimestampMixin):
    """Tracks an auditor's progress through a control's decision-tree workflow."""

    __tablename__ = "workflow_executions"
    __table_args__ = (
        UniqueConstraint(
            "project_id", "framework_control_id", name="uq_workflow_project_control"
        ),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    framework_control_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("framework_controls.id", ondelete="CASCADE"), nullable=False
    )
    answers: Mapped[dict] = mapped_column(JSONB, default=dict)
    current_node_id: Mapped[str] = mapped_column(String(100), nullable=True)
    status: Mapped[WorkflowExecutionStatus] = mapped_column(
        SQLEnum(WorkflowExecutionStatus),
        nullable=False,
        default=WorkflowExecutionStatus.NOT_STARTED,
    )
    generated_finding: Mapped[str] = mapped_column(Text, nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship()
    control: Mapped["FrameworkControl"] = relationship()
