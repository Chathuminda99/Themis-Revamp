from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.config import get_settings
from app.services.auth_service import get_user_from_token


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware to decode session cookie and inject user into request state."""

    async def dispatch(self, request: Request, call_next):
        settings = get_settings()
        session_cookie_name = settings.session_cookie_name

        # Try to get session cookie
        session_token = request.cookies.get(session_cookie_name)
        user = None

        if session_token:
            # Decode token and load user
            user = await get_user_from_token(session_token)

        # Inject user into request state
        request.state.user = user

        return await call_next(request)
