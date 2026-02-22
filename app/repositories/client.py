"""Client repository with search support."""

from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.client import Client
from app.repositories.base import BaseRepository


class ClientRepository(BaseRepository[Client]):
    """Repository for Client model with search capability."""

    model = Client

    def __init__(self, db: Session):
        """Initialize client repository."""
        super().__init__(db)

    def search(self, tenant_id: UUID, query: str) -> List[Client]:
        """Search clients by name, industry, or contact info."""
        if not query or not query.strip():
            return self.get_all(tenant_id)

        search_term = f"%{query.lower()}%"
        return self.db.query(Client).filter(
            and_(
                Client.tenant_id == tenant_id,
                or_(
                    Client.name.ilike(search_term),
                    Client.industry.ilike(search_term),
                    Client.contact_name.ilike(search_term),
                    Client.contact_email.ilike(search_term),
                ),
            )
        ).all()
