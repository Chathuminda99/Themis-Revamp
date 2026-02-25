"""Project repository with filtering and relationships."""

from typing import List
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from app.models.project import Project, ProjectStatus
from app.models.client import Client
from app.models.framework import Framework
from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    """Repository for Project model with filtering and relationships."""

    model = Project

    def __init__(self, db: Session):
        """Initialize project repository."""
        super().__init__(db)

    def get_all_with_details(self, tenant_id: UUID) -> List[Project]:
        """Get all top-level projects for a tenant with eager-loaded client and framework."""
        return self.db.query(Project).filter(
            and_(
                Project.tenant_id == tenant_id,
                Project.parent_project_id.is_(None),
            )
        ).options(
            joinedload(Project.client),
            joinedload(Project.framework)
        ).all()

    def get_by_id_with_details(
        self, tenant_id: UUID, id: UUID
    ) -> Project | None:
        """Get a project by ID with client and framework details."""
        return self.db.query(Project).filter(
            and_(Project.id == id, Project.tenant_id == tenant_id)
        ).options(
            joinedload(Project.client),
            joinedload(Project.framework)
        ).first()

    def get_by_status(
        self, tenant_id: UUID, status: ProjectStatus
    ) -> List[Project]:
        """Get projects filtered by status."""
        return self.db.query(Project).filter(
            and_(
                Project.tenant_id == tenant_id,
                Project.status == status
            )
        ).options(
            joinedload(Project.client),
            joinedload(Project.framework)
        ).all()

    def get_by_client(self, tenant_id: UUID, client_id: UUID) -> List[Project]:
        """Get projects for a specific client."""
        return self.db.query(Project).filter(
            and_(
                Project.tenant_id == tenant_id,
                Project.client_id == client_id
            )
        ).options(
            joinedload(Project.framework)
        ).all()

    def filter_projects(
        self,
        tenant_id: UUID,
        status: ProjectStatus | None = None,
        client_id: UUID | None = None,
        framework_id: UUID | None = None,
        search: str | None = None,
    ) -> List[Project]:
        """Filter top-level projects by optional criteria."""
        query = self.db.query(Project).filter(
            and_(
                Project.tenant_id == tenant_id,
                Project.parent_project_id.is_(None),
            )
        )

        if status:
            query = query.filter(Project.status == status)

        if client_id:
            query = query.filter(Project.client_id == client_id)

        if framework_id:
            query = query.filter(Project.framework_id == framework_id)

        if search and search.strip():
            search_term = f"%{search.lower()}%"
            query = query.filter(Project.name.ilike(search_term))

        return query.options(
            joinedload(Project.client),
            joinedload(Project.framework),
        ).all()

    def get_children(
        self, tenant_id: UUID, parent_project_id: UUID
    ) -> List[Project]:
        """Get all sub-projects (segments) for a parent project."""
        return self.db.query(Project).filter(
            and_(
                Project.tenant_id == tenant_id,
                Project.parent_project_id == parent_project_id,
            )
        ).options(
            joinedload(Project.client),
            joinedload(Project.framework)
        ).all()

    def create_segment(
        self,
        tenant_id: UUID,
        parent_project_id: UUID,
        name: str,
        description: str | None = None,
    ) -> Project:
        """Create a sub-project (segment) under a parent project."""
        parent = self.get_by_id_with_details(tenant_id, parent_project_id)
        if not parent:
            raise ValueError(f"Parent project {parent_project_id} not found")

        segment = self.model(
            tenant_id=tenant_id,
            parent_project_id=parent_project_id,
            client_id=parent.client_id,
            framework_id=parent.framework_id,
            name=name,
            description=description,
            status=ProjectStatus.DRAFT,
        )
        self.db.add(segment)
        self.db.commit()
        self.db.refresh(segment, ["client", "framework"])
        return segment
