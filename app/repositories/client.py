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

    def filter_clients(
        self, tenant_id: UUID, industry: str | None = None, search: str | None = None
    ) -> List[Client]:
        """Filter clients by optional industry and search term."""
        query = self.db.query(Client).filter(Client.tenant_id == tenant_id)

        if industry and industry.strip():
            query = query.filter(Client.industry.ilike(industry))

        if search and search.strip():
            search_term = f"%{search.lower()}%"
            query = query.filter(
                or_(
                    Client.name.ilike(search_term),
                    Client.contact_name.ilike(search_term),
                    Client.contact_email.ilike(search_term),
                )
            )

        return query.all()

    def get_distinct_industries(self, tenant_id: UUID) -> List[str]:
        """Get distinct industries for a tenant, ordered alphabetically."""
        results = self.db.query(Client.industry).filter(
            and_(Client.tenant_id == tenant_id, Client.industry.isnot(None))
        ).distinct().order_by(Client.industry).all()
        return [row[0] for row in results if row[0]]
