# Themis-Revamp: Project Onboarding for Claude Code

## Quick Facts
- **Stack**: FastAPI (Python 3.14.2) + SQLAlchemy + PostgreSQL + Tailwind CSS
- **Database**: PostgreSQL 18.2 local instance
- **Package Managers**: uv (Python), npm (Node.js)
- **Deployment**: Not yet (Phase 1 = local dev foundation)

## Key Implementation Details
- **Session Auth**: itsdangerous URLSafeTimedSerializer, HTTP-only cookies (8-hour max age)
- **Multi-tenancy**: Middleware injects `request.state.tenant` from authenticated user
- **UI**: Dark sidebar (navy `bg-slate-900`) + light main content area + Tailwind CSS v3
- **Database Setup**: Manual `createdb themis_dev` required before migrations

## File Structure Mental Model
- `app/models/` — All SQLAlchemy ORM models + migrations (Alembic handles DB schema)
- `app/routes/` — FastAPI route handlers
- `templates/` — Jinja2 templates (base.html wraps all pages except auth/login.html)
- `static/css/` — Tailwind compiled output (output.css is gitignored, rebuild after pulling)
- `seeds/` — Initial data population scripts

## Workflow Checklist
1. Before starting: activate `.venv` and set `.env` correctly
2. After pulling: `npm run build:css` (rebuild Tailwind)
3. After schema changes: `alembic revision --autogenerate -m "..."` + `alembic upgrade head`
4. Dev server: `uvicorn app.main:app --reload`
5. Watch CSS: `npm run watch:css` (separate terminal)

## Known Constraints
- Python 3.14.2 is bleeding edge; if `psycopg2-binary` fails, use `psycopg[binary]` v3
- Phase 1 seed creates only one tenant + one admin user
- HTMX and Alpine.js loaded from CDN (for development simplicity)
- No test suite in Phase 1

## Common Paths
- Config: `app/config.py`
- Database connection: `app/database.py`
- Authentication logic: `app/services/auth_service.py`
- Base template: `templates/base.html`
- Root factory: `app/main.py`

## Next Phases (Not Yet Implemented)
- Phase 2: Repositories, Client/Framework/Project routes
- Phase 3: Advanced filtering and search
- Phase 4: Report generation
- Phase 5: Test suite + CI/CD
