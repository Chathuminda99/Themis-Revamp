from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ProjectStatus
from app.repositories import (
    ProjectRepository,
    ClientRepository,
    FrameworkRepository,
    ProjectResponseRepository,
)

router = APIRouter(tags=["dashboard"])
from app.templates import templates


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """Render dashboard page."""
    # Check if user is authenticated
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    # Get real stats from repositories
    project_repo = ProjectRepository(db)
    client_repo = ClientRepository(db)
    framework_repo = FrameworkRepository(db)
    response_repo = ProjectResponseRepository(db)

    all_projects = project_repo.get_all(user.tenant_id)
    active_projects = project_repo.get_by_status(user.tenant_id, ProjectStatus.IN_PROGRESS)
    completed_projects = project_repo.get_by_status(user.tenant_id, ProjectStatus.COMPLETED)
    pending_responses = response_repo.count_pending_for_tenant(user.tenant_id)

    stats = {
        "total_projects": len(all_projects),
        "active_projects": len(active_projects),
        "completed_assessments": len(completed_projects),
        "pending_responses": pending_responses,
        "total_clients": len(client_repo.get_all(user.tenant_id)),
        "total_frameworks": len(framework_repo.get_all(user.tenant_id)),
    }

    return templates.TemplateResponse(
        "dashboard/index.html",
        {
            "request": request,
            "user": user,
            "stats": stats,
            "active_projects": active_projects,
        },
    )
