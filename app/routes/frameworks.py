"""Framework management routes (read-only for Phase 2)."""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Framework
from app.repositories import FrameworkRepository

router = APIRouter(prefix="/frameworks", tags=["frameworks"])
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
async def list_frameworks(request: Request, db: Session = Depends(get_db)):
    """List all frameworks for the authenticated tenant."""
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    repo = FrameworkRepository(db)
    frameworks = repo.get_all(user.tenant_id)

    return templates.TemplateResponse(
        "frameworks/list.html",
        {
            "request": request,
            "user": user,
            "frameworks": frameworks,
        },
    )


@router.get("/{framework_id}", response_class=HTMLResponse)
async def detail_framework(
    framework_id: str, request: Request, db: Session = Depends(get_db)
):
    """Show framework detail page with sections and controls tree."""
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    repo = FrameworkRepository(db)
    framework = repo.get_by_id_with_sections(user.tenant_id, framework_id)

    if not framework:
        return RedirectResponse(url="/frameworks", status_code=302)

    return templates.TemplateResponse(
        "frameworks/detail.html",
        {
            "request": request,
            "user": user,
            "framework": framework,
        },
    )
