import secrets
import uuid

import msal
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import SessionLocal
from app.models.user import AuthProvider, User
from app.utils.security import hash_password, session_manager, verify_password

settings = get_settings()


def authenticate_user(email: str, password: str, db: Session) -> User:
    """Authenticate user by email and password."""
    user = db.query(User).filter(User.email == email).first()

    if not user or not user.is_active:
        return None

    if user.password_hash is None:  # Azure AD user, no local password
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


def create_session_token(user: User) -> str:
    """Create a session token for a user."""
    data = {
        "user_id": str(user.id),
        "tenant_id": str(user.tenant_id),
    }
    return session_manager.create_token(data)


async def get_user_from_token(token: str) -> User:
    """Get user from a session token."""
    data = session_manager.decode_token(token)

    if not data:
        return None

    try:
        user_id = uuid.UUID(data.get("user_id"))
    except (ValueError, TypeError):
        return None

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
        return user
    finally:
        db.close()


def _get_msal_app() -> msal.ConfidentialClientApplication:
    """Create an MSAL ConfidentialClientApplication."""
    authority = f"https://login.microsoftonline.com/{settings.azure_ad_tenant_id}"
    return msal.ConfidentialClientApplication(
        client_id=settings.azure_ad_client_id,
        client_credential=settings.azure_ad_client_secret,
        authority=authority,
    )


def _graph_scopes() -> list[str]:
    """Return Graph API scopes (MSAL adds openid/profile/offline_access automatically)."""
    return [s for s in settings.azure_ad_scopes.split() if s not in ("openid", "profile", "offline_access", "email")]


def initiate_azure_flow() -> dict:
    """Start the Azure AD auth code flow with PKCE. Returns the flow dict (contains auth_uri)."""
    app = _get_msal_app()
    return app.initiate_auth_code_flow(
        scopes=_graph_scopes(),
        redirect_uri=settings.azure_ad_redirect_uri,
    )


def exchange_azure_code(flow: dict, auth_response: dict) -> dict | None:
    """Complete the auth code flow. Returns id_token_claims or None on failure."""
    import logging
    logger = logging.getLogger("auditpro.security")
    app = _get_msal_app()
    result = app.acquire_token_by_auth_code_flow(
        auth_code_flow=flow,
        auth_response=auth_response,
    )
    if "error" in result:
        logger.warning("msal_token_exchange_failed error=%s description=%s", result.get("error"), result.get("error_description"))
    if "error" in result:
        return None
    return result.get("id_token_claims")


def get_or_create_azure_user(claims: dict, db: Session) -> User:
    """Look up or create a user from Azure AD token claims.

    Lookup order:
    1. By azure_oid (stable identifier)
    2. By email (link pre-existing local account)
    3. Create new user (is_active=False, pending approval)
    """
    oid = claims.get("oid") or claims.get("sub")
    email = (claims.get("email") or claims.get("preferred_username") or "").lower().strip()
    full_name = claims.get("name") or email

    # 1. Lookup by OID
    if oid:
        user = db.query(User).filter(User.azure_oid == oid).first()
        if user:
            return user

    # 2. Lookup by email (link existing local account)
    if email:
        user = db.query(User).filter(User.email == email).first()
        if user:
            if oid and not user.azure_oid:
                user.azure_oid = oid
                user.auth_provider = AuthProvider.AZURE_AD
                db.commit()
                db.refresh(user)
            return user

    # 3. Create new inactive user
    from app.models.tenant import Tenant

    tenant = (
        db.query(Tenant).filter(Tenant.slug == settings.azure_default_tenant_slug).first()
    )
    if not tenant:
        # Fallback: use the first tenant
        tenant = db.query(Tenant).first()

    user = User(
        tenant_id=tenant.id,
        email=email,
        full_name=full_name,
        password_hash=None,
        auth_provider=AuthProvider.AZURE_AD,
        azure_oid=oid,
        is_active=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
