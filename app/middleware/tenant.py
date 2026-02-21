from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.database import SessionLocal
from app.models import Tenant


class TenantMiddleware(BaseHTTPMiddleware):
    """Middleware to inject tenant into request state from authenticated user."""

    async def dispatch(self, request: Request, call_next):
        tenant = None

        # Get user from request state (set by AuthMiddleware)
        user = getattr(request.state, "user", None)

        if user:
            # Load tenant from database
            db = SessionLocal()
            try:
                tenant = db.query(Tenant).filter(Tenant.id == user.tenant_id).first()
            finally:
                db.close()

        # Inject tenant into request state
        request.state.tenant = tenant

        return await call_next(request)
