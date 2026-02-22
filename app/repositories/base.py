"""Generic base repository for multi-tenant data access."""

from typing import Generic, TypeVar, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Base repository with tenant-scoped CRUD operations."""

    model: type[T] = None

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def get_all(self, tenant_id: UUID) -> List[T]:
        """Get all records for a tenant."""
        if not hasattr(self.model, "tenant_id"):
            raise NotImplementedError(f"{self.model.__name__} does not support tenant_id")
        return self.db.query(self.model).filter(
            self.model.tenant_id == tenant_id
        ).all()

    def get_by_id(self, tenant_id: UUID, id: UUID) -> T | None:
        """Get a single record by ID for a tenant."""
        if not hasattr(self.model, "tenant_id"):
            raise NotImplementedError(f"{self.model.__name__} does not support tenant_id")
        return self.db.query(self.model).filter(
            and_(self.model.id == id, self.model.tenant_id == tenant_id)
        ).first()

    def create(self, **kwargs) -> T:
        """Create a new record (caller must include tenant_id)."""
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def update(self, tenant_id: UUID, id: UUID, **kwargs) -> T | None:
        """Update a record by ID for a tenant."""
        if not hasattr(self.model, "tenant_id"):
            raise NotImplementedError(f"{self.model.__name__} does not support tenant_id")

        instance = self.get_by_id(tenant_id, id)
        if not instance:
            return None

        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        self.db.commit()
        self.db.refresh(instance)
        return instance

    def delete(self, tenant_id: UUID, id: UUID) -> bool:
        """Delete a record by ID for a tenant."""
        if not hasattr(self.model, "tenant_id"):
            raise NotImplementedError(f"{self.model.__name__} does not support tenant_id")

        instance = self.get_by_id(tenant_id, id)
        if not instance:
            return False

        self.db.delete(instance)
        self.db.commit()
        return True
