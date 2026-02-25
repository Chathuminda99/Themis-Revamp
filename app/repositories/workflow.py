"""Repository for workflow execution management."""

from typing import Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.workflow import WorkflowExecution, WorkflowExecutionStatus


class WorkflowExecutionRepository:
    """Repository for WorkflowExecution with project+control scoping."""

    def __init__(self, db: Session):
        self.db = db

    def get_for_project_control(
        self, project_id: UUID, control_id: UUID
    ) -> WorkflowExecution | None:
        """Get workflow execution for a specific project+control pair."""
        return self.db.query(WorkflowExecution).filter(
            and_(
                WorkflowExecution.project_id == project_id,
                WorkflowExecution.framework_control_id == control_id,
            )
        ).first()

    def get_or_create(
        self, project_id: UUID, control_id: UUID
    ) -> WorkflowExecution:
        """Get existing execution or create a new one."""
        execution = self.get_for_project_control(project_id, control_id)
        if not execution:
            execution = WorkflowExecution(
                project_id=project_id,
                framework_control_id=control_id,
                answers={},
                status=WorkflowExecutionStatus.NOT_STARTED,
            )
            self.db.add(execution)
            self.db.commit()
            self.db.refresh(execution)
        return execution

    def upsert_answer(
        self,
        project_id: UUID,
        control_id: UUID,
        node_id: str,
        answer: Any,
        current_node_id: str | None = None,
        status: WorkflowExecutionStatus = WorkflowExecutionStatus.IN_PROGRESS,
        generated_finding: str | None = None,
    ) -> WorkflowExecution:
        """Record an answer for a workflow node."""
        execution = self.get_or_create(project_id, control_id)

        # Merge the new answer into existing answers
        answers = dict(execution.answers) if execution.answers else {}
        answers[node_id] = answer

        execution.answers = answers
        execution.current_node_id = current_node_id
        execution.status = status
        execution.generated_finding = generated_finding

        self.db.commit()
        self.db.refresh(execution)
        return execution

    def reset(self, project_id: UUID, control_id: UUID) -> WorkflowExecution:
        """Reset a workflow execution to start over."""
        execution = self.get_or_create(project_id, control_id)
        execution.answers = {}
        execution.current_node_id = None
        execution.status = WorkflowExecutionStatus.NOT_STARTED
        execution.generated_finding = None
        self.db.commit()
        self.db.refresh(execution)
        return execution
