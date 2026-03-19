# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Stack
- **Backend**: FastAPI (Python 3.14.2) + SQLAlchemy ORM + PostgreSQL 18.2
- **Frontend**: Jinja2 templates + HTMX + Alpine.js (CDN) + Tailwind CSS v3
- **Auth**: itsdangerous URLSafeTimedSerializer, HTTP-only session cookies (8-hour max age)
- **Package managers**: uv (Python), npm (Tailwind only)

## Commands

```bash
# Dev server
source .venv/bin/activate
uvicorn app.main:app --reload

# CSS (separate terminal)
npm run watch:css          # dev
npm run build:css          # one-shot

# After schema changes
alembic revision --autogenerate -m "describe change"
alembic upgrade head

# Seed data (run in order)
python seeds/seed.py                  # tenant, users, frameworks, PCI DSS R2/5/7/8 controls
python seeds/seed_r10_from_excel.py   # PCI DSS R10 controls from Excel
python seeds/seed_health_check.py     # health check review scope types + mappings

# Version is tracked in app/version.py — bump manually on significant changes
```

## Architecture

### Two Project Types
`ProjectType` enum drives which UI/workflow is used:
- `STANDARD_AUDIT` — traditional control response workflow (assign controls → respond → evidence → observations)
- `PCI_DSS_HEALTH_CHECK` — health check workflow (review scopes → sessions → control instances)

Both use the same `Project` model but render completely different templates and use different repositories.

### Health Check Hierarchy
```
Project
  └── ReviewScope  (e.g. "Servers", "Applications")
        └── AuditSession  (a specific asset, e.g. "10.0.0.1 — Web Server")
              └── SessionControlInstance  (one per mapped FrameworkControl)
                    ├── ControlInstanceEvidenceFile
                    └── SessionControlObservation
                          └── SessionControlObservationEvidence
```

`ReviewScopeType` is the global template (tied to a Framework); `ReviewScope` is the project-specific instance. `ControlToReviewScopeMapping` defines which `FrameworkControl`s apply to which `ReviewScopeType`.

### Repository Pattern
All DB access goes through `app/repositories/`. Each domain has its own repo class inheriting from `BaseRepository`. Routes import repos directly — there is no service layer between routes and repos (exception: `app/services/auth_service.py` and `app/services/workflow_engine.py`).

### Multi-tenancy
`TenantMiddleware` runs before `AuthMiddleware`. After auth, `request.state.user` and `request.state.tenant` are available in every route. All queries must be scoped to `tenant_id`.

### HTMX + Alpine.js Patterns
- HTMX handles partial page swaps. Most modals open via `hx-get` → return a `<dialog>` partial.
- `htmx_toast()` in `app/utils/htmx.py` appends `HX-Trigger: {"showMessage": {...}}` headers to trigger the global toast component in `base.html`.
- Alpine.js manages in-page state (dropdowns, tabs, form toggles). Data is defined inline with `x-data`.

### Route → Template Naming
Routes in `app/routes/projects.py` return templates from:
- `templates/projects/` — standard audit pages
- `templates/projects/health_check/` — health check pages
- Partials are prefixed with `_` (e.g. `_control_panel.html`, `_sessions_list.html`)

### Key Files
| Path | Purpose |
|------|---------|
| `app/main.py` | App factory, middleware order, router registration |
| `app/models/health_check.py` | Health check ORM models |
| `app/models/framework.py` | `FrameworkControl` with `assessment_checklist` JSONB |
| `app/repositories/health_check.py` | All health check queries |
| `app/routes/projects.py` | All project + health check routes (single large file) |
| `app/version.py` | Semantic version string |
| `seeds/seed_r10_from_excel.py` | Reads `sample_docs/PCI DSS 4.0_SN_v1.0_Automation.xlsx` |

### assessment_checklist Format
`FrameworkControl.assessment_checklist` and `SessionControlInstance.assessment_checklist_snapshot` use:
```json
{
  "type": "observations",
  "observations": [
    {"id": "obs_1", "label": "Observation text...", "recommendation": "Recommendation text..."}
  ]
}
```

## Known Constraints
- `static/css/output.css` is gitignored — run `npm run build:css` after pulling
- UUID route parameters must be explicitly cast with `uuid.UUID(param)` before passing to repositories
- `openpyxl` must be installed in the venv separately: `uv pip install openpyxl`
- No test suite exists; no CI/CD pipeline
