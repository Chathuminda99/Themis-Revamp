import bcrypt
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from app.config import get_settings


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


class SessionTokenManager:
    """Manage session tokens using itsdangerous."""

    def __init__(self):
        settings = get_settings()
        self.serializer = URLSafeTimedSerializer(settings.secret_key)
        self.max_age = settings.session_cookie_max_age

    def create_token(self, data: dict) -> str:
        """Create a signed session token."""
        return self.serializer.dumps(data)

    def decode_token(self, token: str) -> dict:
        """Decode and verify a session token."""
        try:
            return self.serializer.loads(token, max_age=self.max_age)
        except (BadSignature, SignatureExpired):
            return None


session_manager = SessionTokenManager()
