"""Project management routes."""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Project, ProjectStatus
from app.repositories import ProjectRepository, ClientRepository, FrameworkRepository

router = APIRouter(prefix="/projects", tags=["projects"])
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
async def list_projects(request: Request, db: Session = Depends(get_db)):
    """List all projects for the authenticated tenant."""
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    repo = ProjectRepository(db)
    projects = repo.get_all_with_details(user.tenant_id)

    return templates.TemplateResponse(
        "projects/list.html",
        {
            "request": request,
            "user": user,
            "projects": projects,
        },
    )


@router.get("/new", response_class=HTMLResponse)
async def new_project_form(request: Request, db: Session = Depends(get_db)):
    """Show new project form modal."""
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    client_repo = ClientRepository(db)
    framework_repo = FrameworkRepository(db)

    clients = client_repo.get_all(user.tenant_id)
    frameworks = framework_repo.get_all(user.tenant_id)

    return templates.TemplateResponse(
        "projects/_form.html",
        {
            "request": request,
            "user": user,
            "project": None,
            "clients": clients,
            "frameworks": frameworks,
        },
    )


@router.post("", response_class=HTMLResponse)
async def create_project(request: Request, db: Session = Depends(get_db)):
    """Create a new project."""
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    form_data = await request.form()

    status_value = form_data.get("status", ProjectStatus.DRAFT.value)
    try:
        status = ProjectStatus(status_value)
    except ValueError:
        status = ProjectStatus.DRAFT

    repo = ProjectRepository(db)
    project = repo.create(
        tenant_id=user.tenant_id,
        client_id=form_data.get("client_id"),
        framework_id=form_data.get("framework_id"),
        name=form_data.get("name"),
        description=form_data.get("description"),
        status=status,
    )

    # Refresh to get related objects
    db.refresh(project, ["client", "framework"])

    return templates.TemplateResponse(
        "projects/_row.html",
        {
            "request": request,
            "user": user,
            "project": project,
        },
    )


@router.get("/{project_id}/edit", response_class=HTMLResponse)
async def edit_project_form(
    project_id: str, request: Request, db: Session = Depends(get_db)
):
    """Show edit project form modal."""
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    repo = ProjectRepository(db)
    project = repo.get_by_id_with_details(user.tenant_id, project_id)

    if not project:
        return RedirectResponse(url="/projects", status_code=302)

    client_repo = ClientRepository(db)
    framework_repo = FrameworkRepository(db)

    clients = client_repo.get_all(user.tenant_id)
    frameworks = framework_repo.get_all(user.tenant_id)

    return templates.TemplateResponse(
        "projects/_form.html",
        {
            "request": request,
            "user": user,
            "project": project,
            "clients": clients,
            "frameworks": frameworks,
        },
    )


@router.post("/{project_id}", response_class=HTMLResponse)
async def update_project(
    project_id: str, request: Request, db: Session = Depends(get_db)
):
    """Update an existing project."""
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    form_data = await request.form()

    status_value = form_data.get("status", ProjectStatus.DRAFT.value)
    try:
        status = ProjectStatus(status_value)
    except ValueError:
        status = ProjectStatus.DRAFT

    repo = ProjectRepository(db)
    project = repo.update(
        user.tenant_id,
        project_id,
        name=form_data.get("name"),
        description=form_data.get("description"),
        client_id=form_data.get("client_id"),
        framework_id=form_data.get("framework_id"),
        status=status,
    )

    if not project:
        return RedirectResponse(url="/projects", status_code=302)

    # Refresh to get related objects
    db.refresh(project, ["client", "framework"])

    return templates.TemplateResponse(
        "projects/_row.html",
        {
            "request": request,
            "user": user,
            "project": project,
        },
    )


@router.delete("/{project_id}", response_class=HTMLResponse)
async def delete_project(
    project_id: str, request: Request, db: Session = Depends(get_db)
):
    """Delete a project."""
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    repo = ProjectRepository(db)
    success = repo.delete(user.tenant_id, project_id)

    if success:
        return HTMLResponse("")  # Empty response for successful delete
    return RedirectResponse(url="/projects", status_code=302)


@router.get("/{project_id}", response_class=HTMLResponse)
async def detail_project(
    project_id: str, request: Request, db: Session = Depends(get_db)
):
    """Show project detail page."""
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    repo = ProjectRepository(db)
    project = repo.get_by_id_with_details(user.tenant_id, project_id)

    if not project:
        return RedirectResponse(url="/projects", status_code=302)

    return templates.TemplateResponse(
        "projects/detail.html",
        {
            "request": request,
            "user": user,
            "project": project,
        },
    )
