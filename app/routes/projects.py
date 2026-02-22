"""Project management routes."""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Project, ProjectStatus
from app.models.project import ResponseStatus
from app.repositories import (
    ProjectRepository,
    ClientRepository,
    FrameworkRepository,
    ProjectResponseRepository,
)

router = APIRouter(prefix="/projects", tags=["projects"])
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
async def list_projects(
    request: Request,
    db: Session = Depends(get_db),
    status: str | None = None,
    client_id: str | None = None,
    framework_id: str | None = None,
    q: str | None = None,
):
    """List all projects for the authenticated tenant with optional filtering."""
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    repo = ProjectRepository(db)

    # Convert status string to enum if provided
    status_enum = None
    if status and status.strip():
        try:
            status_enum = ProjectStatus(status)
        except ValueError:
            pass

    # Use filter_projects with optional criteria
    projects = repo.filter_projects(
        user.tenant_id,
        status=status_enum,
        client_id=client_id if client_id and client_id.strip() else None,
        framework_id=framework_id if framework_id and framework_id.strip() else None,
        search=q,
    )

    # Check if this is an HTMX request (filter update)
    is_htmx = request.headers.get("HX-Request") == "true"

    if is_htmx:
        # Return just the table rows
        return templates.TemplateResponse(
            "projects/_projects_table.html",
            {
                "request": request,
                "user": user,
                "projects": projects,
            },
        )

    # Get available filters for the form
    client_repo = ClientRepository(db)
    framework_repo = FrameworkRepository(db)
    all_clients = client_repo.get_all(user.tenant_id)
    all_frameworks = framework_repo.get_all(user.tenant_id)

    # Build active_filters dict for form pre-population
    active_filters = {
        "status": status or "",
        "client_id": client_id or "",
        "framework_id": framework_id or "",
        "q": q or "",
    }

    return templates.TemplateResponse(
        "projects/list.html",
        {
            "request": request,
            "user": user,
            "projects": projects,
            "all_clients": all_clients,
            "all_frameworks": all_frameworks,
            "active_filters": active_filters,
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

    # Validate required fields
    client_id = (form_data.get("client_id") or "").strip()
    framework_id = (form_data.get("framework_id") or "").strip()
    name = (form_data.get("name") or "").strip()

    if not client_id or not framework_id or not name:
        # Return to form with error (for now, just redirect)
        return RedirectResponse(url="/projects/new", status_code=302)

    status_value = form_data.get("status", ProjectStatus.DRAFT.value)
    try:
        status = ProjectStatus(status_value)
    except ValueError:
        status = ProjectStatus.DRAFT

    repo = ProjectRepository(db)
    project = repo.create(
        tenant_id=user.tenant_id,
        client_id=client_id,
        framework_id=framework_id,
        name=name,
        description=form_data.get("description", ""),
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

    # Validate required fields
    client_id = (form_data.get("client_id") or "").strip()
    framework_id = (form_data.get("framework_id") or "").strip()
    name = (form_data.get("name") or "").strip()

    if not client_id or not framework_id or not name:
        # Return to form with error (for now, just redirect)
        return RedirectResponse(url=f"/projects/{project_id}/edit", status_code=302)

    status_value = form_data.get("status", ProjectStatus.DRAFT.value)
    try:
        status = ProjectStatus(status_value)
    except ValueError:
        status = ProjectStatus.DRAFT

    repo = ProjectRepository(db)
    project = repo.update(
        user.tenant_id,
        project_id,
        name=name,
        description=form_data.get("description", ""),
        client_id=client_id,
        framework_id=framework_id,
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


@router.get("/{project_id}/controls/{control_id}/row", response_class=HTMLResponse)
async def get_control_row(
    project_id: str, control_id: str, request: Request, db: Session = Depends(get_db)
):
    """Get control row (for cancel/refresh in forms)."""
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    repo = ProjectRepository(db)
    project = repo.get_by_id_with_details(user.tenant_id, project_id)

    if not project:
        return RedirectResponse(url="/projects", status_code=302)

    # Load framework with sections and controls
    framework_repo = FrameworkRepository(db)
    framework = framework_repo.get_by_id_with_sections(user.tenant_id, project.framework_id)

    # Find the control in the framework
    control = None
    if framework:
        for section in framework.sections:
            for ctrl in section.controls:
                if str(ctrl.id) == control_id:
                    control = ctrl
                    break
            if control:
                break

    if not control:
        return RedirectResponse(url=f"/projects/{project_id}", status_code=302)

    # Get all responses for this project
    response_repo = ProjectResponseRepository(db)
    all_responses = response_repo.get_for_project(project.id)
    responses_dict = {str(resp.framework_control_id): resp for resp in all_responses}

    return templates.TemplateResponse(
        "projects/_control_row.html",
        {
            "request": request,
            "user": user,
            "project": project,
            "control": control,
            "responses": responses_dict,
        },
    )


@router.get("/{project_id}/controls/{control_id}/response", response_class=HTMLResponse)
async def get_control_response_form(
    project_id: str, control_id: str, request: Request, db: Session = Depends(get_db)
):
    """Get control response form (HTMX endpoint)."""
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    repo = ProjectRepository(db)
    project = repo.get_by_id_with_details(user.tenant_id, project_id)

    if not project:
        return RedirectResponse(url="/projects", status_code=302)

    # Load framework with sections and controls
    framework_repo = FrameworkRepository(db)
    framework = framework_repo.get_by_id_with_sections(user.tenant_id, project.framework_id)

    # Find the control in the framework
    control = None
    if framework:
        for section in framework.sections:
            for ctrl in section.controls:
                if str(ctrl.id) == control_id:
                    control = ctrl
                    break
            if control:
                break

    if not control:
        return RedirectResponse(url=f"/projects/{project_id}", status_code=302)

    # Get the response if it exists
    response_repo = ProjectResponseRepository(db)
    response = response_repo.get_by_control(project.id, control.id)

    return templates.TemplateResponse(
        "projects/_control_response_form.html",
        {
            "request": request,
            "user": user,
            "project": project,
            "control": control,
            "response": response,
        },
    )


@router.post("/{project_id}/controls/{control_id}/response", response_class=HTMLResponse)
async def save_control_response(
    project_id: str, control_id: str, request: Request, db: Session = Depends(get_db)
):
    """Save control response (HTMX endpoint)."""
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    repo = ProjectRepository(db)
    project = repo.get_by_id_with_details(user.tenant_id, project_id)

    if not project:
        return RedirectResponse(url="/projects", status_code=302)

    form_data = await request.form()
    response_text = form_data.get("response_text")
    status_value = form_data.get("status", ResponseStatus.NOT_STARTED.value)

    try:
        status = ResponseStatus(status_value)
    except ValueError:
        status = ResponseStatus.NOT_STARTED

    # Upsert the response
    response_repo = ProjectResponseRepository(db)
    response_repo.upsert(project.id, control_id, response_text, status)

    # Load framework with sections and controls to get the control
    framework_repo = FrameworkRepository(db)
    framework = framework_repo.get_by_id_with_sections(user.tenant_id, project.framework_id)

    # Find the control in the framework
    control = None
    if framework:
        for section in framework.sections:
            for ctrl in section.controls:
                if str(ctrl.id) == control_id:
                    control = ctrl
                    break
            if control:
                break

    if not control:
        return RedirectResponse(url=f"/projects/{project_id}", status_code=302)

    # Return the updated row
    return templates.TemplateResponse(
        "projects/_control_row.html",
        {
            "request": request,
            "user": user,
            "project": project,
            "control": control,
            "responses": {str(control.id): response_repo.get_by_control(project.id, control.id)},
        },
    )


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

    # Load framework with sections and controls
    framework_repo = FrameworkRepository(db)
    framework = framework_repo.get_by_id_with_sections(user.tenant_id, project.framework_id)

    # Load all responses for the project
    response_repo = ProjectResponseRepository(db)
    all_responses = response_repo.get_for_project(project.id)
    responses_dict = {str(resp.framework_control_id): resp for resp in all_responses}

    # Calculate progress
    total_controls = 0
    responded_count = 0
    if framework:
        for section in framework.sections:
            total_controls += len(section.controls)
            for control in section.controls:
                if str(control.id) in responses_dict:
                    responded_count += 1

    progress_pct = (responded_count / total_controls * 100) if total_controls > 0 else 0

    return templates.TemplateResponse(
        "projects/detail.html",
        {
            "request": request,
            "user": user,
            "project": project,
            "framework": framework,
            "responses": responses_dict,
            "progress_pct": progress_pct,
            "responded_count": responded_count,
            "total_controls": total_controls,
        },
    )
