"""Framework repository with eager loading of sections and controls."""

from typing import List
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from app.models.framework import Framework, FrameworkSection, FrameworkControl
from app.repositories.base import BaseRepository


class FrameworkRepository(BaseRepository[Framework]):
    """Repository for Framework model with section/control relationships."""

    model = Framework

    def __init__(self, db: Session):
        """Initialize framework repository."""
        super().__init__(db)

    def get_all_with_sections(self, tenant_id: UUID) -> List[Framework]:
        """Get all frameworks for a tenant with eager-loaded sections."""
        return self.db.query(Framework).filter(
            Framework.tenant_id == tenant_id
        ).options(
            joinedload(Framework.sections)
        ).all()

    def get_by_id_with_sections(
        self, tenant_id: UUID, id: UUID
    ) -> Framework | None:
        """Get a framework by ID with eager-loaded sections and controls."""
        return self.db.query(Framework).filter(
            Framework.tenant_id == tenant_id,
            Framework.id == id
        ).options(
            joinedload(Framework.sections)
            .joinedload(FrameworkSection.controls)
        ).first()


# Add relationships to Framework model (these would be defined in the model file)
# For now, they're assumed to exist based on the FK structure
