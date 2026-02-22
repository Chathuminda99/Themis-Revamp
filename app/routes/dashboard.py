from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ProjectStatus
from app.repositories import ProjectRepository, ClientRepository, FrameworkRepository

router = APIRouter(tags=["dashboard"])
templates = Jinja2Templates(directory="templates")


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

    all_projects = project_repo.get_all(user.tenant_id)
    active_projects = project_repo.get_by_status(user.tenant_id, ProjectStatus.IN_PROGRESS)
    completed_projects = project_repo.get_by_status(user.tenant_id, ProjectStatus.COMPLETED)

    stats = {
        "total_projects": len(all_projects),
        "active_projects": len(active_projects),
        "completed_assessments": len(completed_projects),
        "pending_responses": 0,  # TODO: Calculate from project_responses
        "total_clients": len(client_repo.get_all(user.tenant_id)),
        "total_frameworks": len(framework_repo.get_all(user.tenant_id)),
    }

    return templates.TemplateResponse(
        "dashboard/index.html",
        {
            "request": request,
            "user": user,
            "stats": stats,
        },
    )
