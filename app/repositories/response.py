"""Project response repository for managing control responses."""

from typing import List
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from app.models.project import ProjectResponse, ResponseStatus
from app.models.project import Project
from app.repositories.base import BaseRepository


class ProjectResponseRepository(BaseRepository[ProjectResponse]):
    """Repository for ProjectResponse model with project context."""

    model = ProjectResponse

    def __init__(self, db: Session):
        """Initialize response repository."""
        super().__init__(db)

    def get_for_project(self, project_id: UUID) -> List[ProjectResponse]:
        """Get all responses for a project with eager-loaded control."""
        return self.db.query(ProjectResponse).filter(
            ProjectResponse.project_id == project_id
        ).options(
            joinedload(ProjectResponse.control)
        ).all()

    def get_by_control(
        self, project_id: UUID, control_id: UUID
    ) -> ProjectResponse | None:
        """Get response for a specific control in a project."""
        return self.db.query(ProjectResponse).filter(
            and_(
                ProjectResponse.project_id == project_id,
                ProjectResponse.framework_control_id == control_id,
            )
        ).first()

    def upsert(
        self,
        project_id: UUID,
        control_id: UUID,
        response_text: str | None = None,
        status: ResponseStatus = ResponseStatus.NOT_STARTED,
    ) -> ProjectResponse:
        """Create or update a response for a control."""
        response = self.get_by_control(project_id, control_id)

        if response:
            response.response_text = response_text
            response.status = status
            self.db.commit()
            self.db.refresh(response)
        else:
            response = self.model(
                project_id=project_id,
                framework_control_id=control_id,
                response_text=response_text,
                status=status,
            )
            self.db.add(response)
            self.db.commit()
            self.db.refresh(response)

        return response

    def count_pending_for_tenant(self, tenant_id: UUID) -> int:
        """Count pending/in_progress responses for a tenant across all projects."""
        return self.db.query(ProjectResponse).join(
            Project, ProjectResponse.project_id == Project.id
        ).filter(
            and_(
                Project.tenant_id == tenant_id,
                ProjectResponse.status.in_(
                    [ResponseStatus.NOT_STARTED, ResponseStatus.IN_PROGRESS]
                ),
            )
        ).count()
