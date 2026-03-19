"""Repository for persisted per-user form drafts."""

from uuid import UUID

from sqlalchemy import and_

from app.models.form_draft import FormDraft
from app.repositories.base import BaseRepository


class FormDraftRepository(BaseRepository[FormDraft]):
    """Data access for server-side autosaved form drafts."""

    model = FormDraft

    def get_by_key(
        self,
        tenant_id: UUID,
        user_id: UUID,
        draft_key: str,
    ) -> FormDraft | None:
        """Get a stored draft by its stable form key."""
        return self.db.query(FormDraft).filter(
            and_(
                FormDraft.tenant_id == tenant_id,
                FormDraft.user_id == user_id,
                FormDraft.draft_key == draft_key,
            )
        ).first()

    def upsert(
        self,
        tenant_id: UUID,
        user_id: UUID,
        draft_key: str,
        payload_json: str,
        path: str | None = None,
        form_action: str | None = None,
    ) -> FormDraft:
        """Create or update a persisted draft for the current user."""
        draft = self.get_by_key(tenant_id, user_id, draft_key)
        if draft is None:
            draft = FormDraft(
                tenant_id=tenant_id,
                user_id=user_id,
                draft_key=draft_key,
                path=path,
                form_action=form_action,
                payload_json=payload_json,
            )
            self.db.add(draft)
        else:
            draft.path = path
            draft.form_action = form_action
            draft.payload_json = payload_json

        self.db.commit()
        self.db.refresh(draft)
        return draft

    def clear_by_key(
        self,
        tenant_id: UUID,
        user_id: UUID,
        draft_key: str,
    ) -> bool:
        """Delete a persisted draft by key for the current user."""
        draft = self.get_by_key(tenant_id, user_id, draft_key)
        if draft is None:
            return False

        self.db.delete(draft)
        self.db.commit()
        return True
