from sqlalchemy.orm import Session
from app.models import User
from app.utils.security import hash_password, verify_password, session_manager
from app.database import SessionLocal
import uuid


def authenticate_user(email: str, password: str, db: Session) -> User:
    """Authenticate user by email and password."""
    user = db.query(User).filter(User.email == email).first()

    if not user or not user.is_active:
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
        user = db.query(User).filter(User.id == user_id).first()
        return user
    finally:
        db.close()
