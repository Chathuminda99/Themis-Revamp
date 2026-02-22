"""Client management routes."""

from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Client
from app.repositories import ClientRepository

router = APIRouter(prefix="/clients", tags=["clients"])
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
async def list_clients(request: Request, db: Session = Depends(get_db)):
    """List all clients for the authenticated tenant."""
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    repo = ClientRepository(db)
    clients = repo.get_all(user.tenant_id)

    return templates.TemplateResponse(
        "clients/list.html",
        {
            "request": request,
            "user": user,
            "clients": clients,
        },
    )


@router.get("/{client_id}", response_class=HTMLResponse)
async def detail_client(
    client_id: str, request: Request, db: Session = Depends(get_db)
):
    """Show client detail page."""
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    repo = ClientRepository(db)
    client = repo.get_by_id(user.tenant_id, client_id)

    if not client:
        return RedirectResponse(url="/clients", status_code=302)

    return templates.TemplateResponse(
        "clients/detail.html",
        {
            "request": request,
            "user": user,
            "client": client,
        },
    )


@router.get("/new", response_class=HTMLResponse)
async def new_client_form(request: Request, db: Session = Depends(get_db)):
    """Show new client form modal."""
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    return templates.TemplateResponse(
        "clients/_form.html",
        {
            "request": request,
            "user": user,
            "client": None,
        },
    )


@router.post("", response_class=HTMLResponse)
async def create_client(request: Request, db: Session = Depends(get_db)):
    """Create a new client."""
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    form_data = await request.form()

    repo = ClientRepository(db)
    client = repo.create(
        tenant_id=user.tenant_id,
        name=form_data.get("name"),
        industry=form_data.get("industry"),
        contact_name=form_data.get("contact_name"),
        contact_email=form_data.get("contact_email"),
        notes=form_data.get("notes"),
    )

    return templates.TemplateResponse(
        "clients/_row.html",
        {
            "request": request,
            "user": user,
            "client": client,
        },
    )


@router.get("/{client_id}/edit", response_class=HTMLResponse)
async def edit_client_form(
    client_id: str, request: Request, db: Session = Depends(get_db)
):
    """Show edit client form modal."""
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    repo = ClientRepository(db)
    client = repo.get_by_id(user.tenant_id, client_id)

    if not client:
        return RedirectResponse(url="/clients", status_code=302)

    return templates.TemplateResponse(
        "clients/_form.html",
        {
            "request": request,
            "user": user,
            "client": client,
        },
    )


@router.post("/{client_id}", response_class=HTMLResponse)
async def update_client(
    client_id: str, request: Request, db: Session = Depends(get_db)
):
    """Update an existing client."""
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    form_data = await request.form()

    repo = ClientRepository(db)
    client = repo.update(
        user.tenant_id,
        client_id,
        name=form_data.get("name"),
        industry=form_data.get("industry"),
        contact_name=form_data.get("contact_name"),
        contact_email=form_data.get("contact_email"),
        notes=form_data.get("notes"),
    )

    if not client:
        return RedirectResponse(url="/clients", status_code=302)

    return templates.TemplateResponse(
        "clients/_row.html",
        {
            "request": request,
            "user": user,
            "client": client,
        },
    )


@router.delete("/{client_id}", response_class=HTMLResponse)
async def delete_client(
    client_id: str, request: Request, db: Session = Depends(get_db)
):
    """Delete a client."""
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    repo = ClientRepository(db)
    success = repo.delete(user.tenant_id, client_id)

    if success:
        return HTMLResponse("")  # Empty response for successful delete
    return RedirectResponse(url="/clients", status_code=302)


@router.get("/search", response_class=HTMLResponse)
async def search_clients(
    q: str = "", request: Request = None, db: Session = Depends(get_db)
):
    """Search clients for autocomplete (HTMX endpoint)."""
    if not request:
        return HTMLResponse("")

    user = getattr(request.state, "user", None)
    if not user:
        return HTMLResponse("")

    repo = ClientRepository(db)
    results = repo.search(user.tenant_id, q) if q else []

    return templates.TemplateResponse(
        "clients/_search_results.html",
        {
            "request": request,
            "user": user,
            "results": results,
            "query": q,
        },
    )
