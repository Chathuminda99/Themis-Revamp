# Themis — Implementation Plan

---

## 1. System Architecture

### High-Level Architecture

Themis follows a **server-rendered monolith** pattern — FastAPI serves HTML via Jinja2 templates, enhanced with HTMX for dynamic partial updates and Alpine.js for client-side micro-interactions. This avoids the complexity of a separate SPA while delivering a responsive UX.

```
┌─────────────────────────────────────────────────┐
│                   Browser                        │
│  Jinja2 HTML + HTMX + Alpine.js + Tailwind CSS  │
└──────────────────────┬──────────────────────────┘
                       │ HTTP (HTML partials + JSON)
┌──────────────────────▼──────────────────────────┐
│              FastAPI Application                  │
│  ┌───────────┬───────────┬────────────────────┐  │
│  │  Routes   │ Services  │  Report Engine     │  │
│  │ (Views)   │ (Logic)   │  (Jinja2 → PDF)   │  │
│  └───────────┴───────────┴────────────────────┘  │
│  ┌───────────┬───────────┬────────────────────┐  │
│  │   Auth    │ Tenant    │  Framework Engine  │  │
│  │Middleware │ Context   │  (DB-driven)       │  │
│  └───────────┴───────────┴────────────────────┘  │
└──────────────────────┬──────────────────────────┘
                       │ SQLAlchemy (async)
┌──────────────────────▼──────────────────────────┐
│               PostgreSQL                         │
│  (Row-Level Security via tenant_id filtering)    │
└─────────────────────────────────────────────────┘
```

### Component Breakdown

| Component | Responsibility |
|---|---|
| **Routes/Views** | Handle HTTP requests, render templates, return HTMX partials |
| **Services** | Business logic layer — no HTTP or DB coupling |
| **Repositories** | Database access via SQLAlchemy, enforce tenant scoping |
| **Auth Middleware** | Session-based auth, inject current user + tenant into request state |
| **Tenant Context** | Middleware that resolves tenant from session and scopes all queries |
| **Framework Engine** | Loads framework structures from DB, generates project checklists |
| **Report Engine** | Renders audit reports to HTML (Jinja2) and PDF (WeasyPrint) |

### Key Architectural Decisions

- **Server-rendered with HTMX** rather than SPA: Simpler stack, fewer moving parts, better for form-heavy audit workflows. HTMX provides SPA-like feel where needed.
- **Synchronous SQLAlchemy** (not async): For MVP, sync is simpler to debug and reason about. FastAPI supports sync route handlers fine. Can migrate to async later if needed.
- **No ORM-level multi-tenancy magic**: Explicit `tenant_id` filtering at the repository layer. Simple, auditable, no hidden behavior.

### Tech Stack & Core Dependencies

**Backend**
- FastAPI (web framework)
- SQLAlchemy (ORM, sync mode)
- PostgreSQL (database)
- Alembic (database migrations)
- bcrypt (password hashing)
- itsdangerous or starsessions (session management)

**Report Generation**
- Jinja2 (templating engine)
- WeasyPrint (HTML to PDF conversion)
- openpyxl (Excel workbook generation)

**Frontend**
- Jinja2 (server-side templating)
- HTMX (dynamic interactions)
- Alpine.js (lightweight client-side reactivity)
- Tailwind CSS (styling)

**Utilities**
- Pydantic (data validation)
- python-multipart (form file uploads)
- Pillow (image handling for logos)

---

## 2. Module-Wise Design

### Module: Auth
- User registration (tenant admin only), login, logout
- Session-based authentication using signed cookies (via `itsdangerous` or FastAPI sessions)
- Role-based access: **Tenant Admin**, **Auditor**, **Viewer**
- Password hashing with `bcrypt`

### Module: Tenants
- Tenant CRUD (superadmin only for creation)
- Tenant settings (company name, logo, report branding)
- All data queries scoped by `tenant_id`

### Module: Users
- User management within a tenant
- Role assignment
- Profile management

### Module: Clients
- Client organizations that the audit company serves
- Fields: name, industry, contact info, notes
- Scoped to tenant

### Module: Frameworks
- CRUD for compliance frameworks (admin-managed)
- Hierarchical structure: Framework → Section → Control → Checklist Item
- Frameworks can be **global** (shared across tenants, read-only) or **tenant-specific** (custom)
- Import/export capability (JSON format for seeding)

### Module: Projects
- Represents a single audit engagement
- Links: tenant, client, framework, assigned users
- Status workflow: Draft → In Progress → Review → Completed → Archived
- When a project is created, the system **snapshots** the framework's checklist items into project-specific responses (so framework changes don't retroactively alter active audits)

### Module: Audit Execution
- Checklist response management per project
- Each response tracks: status, evidence (text + file references), remarks, risk level
- Progress tracking (% complete per section, per project)
- Filtering and bulk operations on checklist items

### Module: Reports
- Report generation from project data
- Template-based rendering (Jinja2 report templates)
- Output: HTML preview, PDF download, Excel workbook
- Customizable report sections per tenant

### Module: Dashboard
- Tenant-level overview: active projects, completion rates
- Project-level: checklist progress, findings summary
- Simple stats — no complex BI

---

## 3. Database Schema Design

### Core Tables

**tenants**
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| name | VARCHAR(255) | Company name |
| slug | VARCHAR(100) | URL-friendly identifier, unique |
| logo_url | TEXT | Nullable |
| settings | JSONB | Branding, report defaults |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

**users**
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| tenant_id | UUID (FK → tenants) | |
| email | VARCHAR(255) | Unique per tenant |
| password_hash | VARCHAR(255) | |
| full_name | VARCHAR(255) | |
| role | ENUM('admin','auditor','viewer') | |
| is_active | BOOLEAN | |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

**clients**
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| tenant_id | UUID (FK → tenants) | |
| name | VARCHAR(255) | |
| industry | VARCHAR(100) | Nullable |
| contact_name | VARCHAR(255) | Nullable |
| contact_email | VARCHAR(255) | Nullable |
| notes | TEXT | Nullable |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

### Framework Tables

**frameworks**
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| tenant_id | UUID (FK → tenants) | NULL = global/shared framework |
| name | VARCHAR(255) | e.g. "PCI DSS v4.0" |
| code | VARCHAR(50) | e.g. "PCI_DSS_4" |
| version | VARCHAR(20) | |
| description | TEXT | |
| is_active | BOOLEAN | |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

**framework_sections**
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| framework_id | UUID (FK → frameworks) | |
| parent_section_id | UUID (FK → self) | Nullable, for nested sections |
| code | VARCHAR(50) | e.g. "1", "1.1" |
| title | VARCHAR(500) | |
| description | TEXT | |
| sort_order | INTEGER | |

**framework_controls**
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| section_id | UUID (FK → framework_sections) | |
| code | VARCHAR(50) | e.g. "1.1.1" |
| title | VARCHAR(500) | |
| description | TEXT | |
| guidance | TEXT | Implementation guidance |
| sort_order | INTEGER | |

**checklist_items**
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| control_id | UUID (FK → framework_controls) | |
| code | VARCHAR(50) | |
| question | TEXT | The actual checklist question |
| expected_evidence | TEXT | What evidence is expected |
| sort_order | INTEGER | |

### Project Tables

**projects**
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| tenant_id | UUID (FK → tenants) | |
| client_id | UUID (FK → clients) | |
| framework_id | UUID (FK → frameworks) | |
| name | VARCHAR(255) | |
| audit_type | VARCHAR(100) | e.g. "Initial", "Surveillance", "Recertification" |
| status | ENUM('draft','in_progress','review','completed','archived') | |
| report_date | DATE | |
| scope_description | TEXT | |
| created_by | UUID (FK → users) | |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

**project_members**
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| project_id | UUID (FK → projects) | |
| user_id | UUID (FK → users) | |
| role | VARCHAR(50) | e.g. "lead_auditor", "auditor", "reviewer" |

**project_responses** (the core audit execution table)
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| project_id | UUID (FK → projects) | |
| checklist_item_id | UUID (FK → checklist_items) | |
| status | ENUM('not_started','compliant','non_compliant','partially_compliant','not_applicable') | |
| risk_level | ENUM('low','medium','high','critical') | Nullable |
| evidence | TEXT | |
| remarks | TEXT | |
| responded_by | UUID (FK → users) | |
| responded_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

**project_evidence_files**
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| response_id | UUID (FK → project_responses) | |
| filename | VARCHAR(255) | |
| file_path | TEXT | Server path |
| file_size | INTEGER | |
| mime_type | VARCHAR(100) | |
| uploaded_by | UUID (FK → users) | |
| uploaded_at | TIMESTAMP | |

### Relationships Diagram (text)

```
tenants 1──N users
tenants 1──N clients
tenants 1──N projects
tenants 1──N frameworks (tenant-specific)

frameworks 1──N framework_sections
framework_sections 1──N framework_sections (self-ref for nesting)
framework_sections 1──N framework_controls
framework_controls 1──N checklist_items

clients 1──N projects
frameworks 1──N projects
projects N──N users (via project_members)
projects 1──N project_responses
checklist_items 1──N project_responses
project_responses 1──N project_evidence_files
```

### Indexes (Critical)

- `project_responses(project_id, checklist_item_id)` — UNIQUE, prevents duplicate responses
- `project_responses(project_id, status)` — for progress aggregation
- `users(tenant_id, email)` — UNIQUE
- `frameworks(tenant_id)` — for tenant-scoped framework queries
- `projects(tenant_id, status)` — dashboard queries
- All foreign keys indexed by default

---

## 4. API Structure

### Auth Routes (`/auth`)

| Method | Path | Responsibility |
|---|---|---|
| GET | `/auth/login` | Render login page |
| POST | `/auth/login` | Authenticate, create session |
| POST | `/auth/logout` | Destroy session |

### Dashboard Routes (`/dashboard`)

| Method | Path | Responsibility |
|---|---|---|
| GET | `/dashboard` | Tenant dashboard with project overview stats |

### Client Routes (`/clients`)

| Method | Path | Responsibility |
|---|---|---|
| GET | `/clients` | List clients (full page) |
| GET | `/clients/new` | Render create form |
| POST | `/clients` | Create client |
| GET | `/clients/{id}` | Client detail page |
| GET | `/clients/{id}/edit` | Render edit form (HTMX partial) |
| PUT | `/clients/{id}` | Update client |
| DELETE | `/clients/{id}` | Delete client |

### Framework Routes (`/frameworks`)

| Method | Path | Responsibility |
|---|---|---|
| GET | `/frameworks` | List frameworks |
| GET | `/frameworks/{id}` | Framework detail — show section/control/item tree |
| GET | `/frameworks/{id}/sections/{sid}` | Section detail (HTMX partial for lazy-loading tree) |
| POST | `/frameworks` | Create framework (admin) |
| POST | `/frameworks/{id}/sections` | Add section |
| POST | `/frameworks/{id}/controls` | Add control under section |
| POST | `/frameworks/{id}/items` | Add checklist item under control |
| PUT/DELETE | (corresponding edit/delete routes) | |
| POST | `/frameworks/import` | Import framework from JSON |
| GET | `/frameworks/{id}/export` | Export framework as JSON |

### Project Routes (`/projects`)

| Method | Path | Responsibility |
|---|---|---|
| GET | `/projects` | List projects with filters |
| GET | `/projects/new` | Create project form |
| POST | `/projects` | Create project (triggers checklist snapshot) |
| GET | `/projects/{id}` | Project overview page |
| GET | `/projects/{id}/edit` | Edit project metadata |
| PUT | `/projects/{id}` | Update project |
| PUT | `/projects/{id}/status` | Transition project status |

### Audit Execution Routes (`/projects/{id}/audit`)

| Method | Path | Responsibility |
|---|---|---|
| GET | `/projects/{id}/audit` | Audit execution page — show sections tree + checklist |
| GET | `/projects/{id}/audit/section/{sid}` | Load section's checklist items (HTMX partial) |
| PUT | `/projects/{id}/audit/response/{rid}` | Update a single response (status, evidence, remarks) |
| POST | `/projects/{id}/audit/response/{rid}/evidence` | Upload evidence file |
| DELETE | `/projects/{id}/audit/evidence/{eid}` | Remove evidence file |
| GET | `/projects/{id}/audit/progress` | Progress stats (HTMX partial for live update) |

### Report Routes (`/projects/{id}/report`)

| Method | Path | Responsibility |
|---|---|---|
| GET | `/projects/{id}/report` | Report preview (HTML) |
| GET | `/projects/{id}/report/pdf` | Download PDF |
| GET | `/projects/{id}/report/excel` | Download Excel workbook |
| GET | `/projects/{id}/report/settings` | Report customization form |
| PUT | `/projects/{id}/report/settings` | Save report customization |

### User Management Routes (`/users`)

| Method | Path | Responsibility |
|---|---|---|
| GET | `/users` | List users (admin only) |
| POST | `/users` | Create user |
| PUT | `/users/{id}` | Update user |
| DELETE | `/users/{id}` | Deactivate user |

### Tenant Settings (`/settings`)

| Method | Path | Responsibility |
|---|---|---|
| GET | `/settings` | Tenant settings page |
| PUT | `/settings` | Update tenant settings |

---

## 5. Frontend Interaction Approach

### HTMX Usage

HTMX handles all dynamic server interactions without JavaScript API calls:

| Pattern | Where Used |
|---|---|
| **Partial page swap** (`hx-get`, `hx-swap="innerHTML"`) | Loading section checklists in audit view, loading edit forms inline |
| **Form submission** (`hx-post`, `hx-put`) | All create/update operations — forms submit via HTMX, server returns updated HTML partial |
| **Inline editing** (`hx-trigger="click"`, swap edit form) | Checklist response fields — click to edit status/remarks, save inline |
| **Lazy loading** (`hx-trigger="revealed"`) | Framework tree nodes — load child sections on expand |
| **Live search/filter** (`hx-get` with `hx-trigger="keyup changed delay:300ms"`) | Client list, project list filtering |
| **Progress update** (`hx-get` with `hx-trigger="every 30s"` or after response save) | Audit progress bar refreshes after each response save |
| **Delete confirmation** (via `hx-confirm`) | Delete actions get browser-native confirm dialog |
| **Out-of-band swaps** (`hx-swap-oob`) | After saving a response, update both the row AND the progress bar in a single response |

### Alpine.js Usage

Alpine handles **client-only** interactivity that doesn't need server round-trips:

| Pattern | Where Used |
|---|---|
| **Dropdowns/menus** (`x-show`, `@click.away`) | Navigation dropdowns, action menus |
| **Tabs** (`x-data="{ tab: 'overview' }"`) | Project detail tabs (overview, audit, report) |
| **Accordion/tree expand** (`x-show`, `x-transition`) | Framework section tree expand/collapse |
| **Form validation feedback** (`:class` binding) | Highlight required fields before submit |
| **Modal dialogs** (`x-show` + `x-transition`) | Confirmation modals, file upload preview |
| **Sidebar toggle** | Responsive sidebar collapse on mobile |
| **Bulk selection** (`x-data` with checkbox tracking) | Select multiple checklist items for bulk status update |

### Template Strategy

- **Base layout** (`base.html`): Shell with nav, sidebar, content area, Tailwind/HTMX/Alpine includes
- **Full pages**: Extend base layout, rendered on full navigation
- **Partials** (`partials/`): Fragments returned by HTMX requests — no `<html>` wrapper, just the component HTML
- Server detects HTMX requests via `HX-Request` header and returns partial vs full page accordingly

---

## 6. Multi-Tenancy Strategy

### Approach: Application-Level Row Filtering (Shared Schema)

All tenants share one database and one schema. Every tenant-scoped table has a `tenant_id` column.

**Why this approach:**
- Simplest to implement and operate for MVP
- Single database to back up, migrate, monitor
- Adequate isolation for a B2B audit tool (not handling adversarial tenants)
- Can evolve to schema-per-tenant later if needed

### Enforcement Layers

1. **Session**: On login, `tenant_id` is stored in the session. Middleware injects it into `request.state.tenant_id`.

2. **Repository layer**: Every repository method that touches tenant-scoped data includes `WHERE tenant_id = :tenant_id`. This is the **primary enforcement point**.

3. **Base repository class**: A `TenantScopedRepository` base class that automatically applies tenant filtering to all queries. Individual repositories extend this.

4. **No cross-tenant data access**: No API endpoint allows specifying a different `tenant_id`. It always comes from the session.

5. **Global data**: Frameworks with `tenant_id = NULL` are global (shared). Tenants can read them but not modify them. Tenants can create their own frameworks (`tenant_id` set).

### What is NOT tenant-scoped

- Global frameworks (shared compliance standards)
- System configuration
- Superadmin operations (future: manage tenants)

---

## 7. Report Generation Design

### Architecture

```
Project Data (DB) → Report Data Assembler → Multiple Output Formats
                                    ├─→ Jinja2 Report Template → HTML (preview)
                                    ├─→ Jinja2 Report Template → HTML → WeasyPrint → PDF
                                    └─→ openpyxl Workbook → Excel (.xlsx)
```

### Report Data Assembler

A service that queries all project-related data and assembles it into a structured dict:

- **Project metadata**: client, framework, dates, auditors
- **Executive summary**: auto-generated stats (% compliant, # findings by risk level)
- **Scope**: from project's scope_description
- **Findings**: all non-compliant / partially-compliant responses, grouped by section, with risk levels
- **Recommendations**: derived from findings (initially manual via remarks; future: AI-assisted)
- **Statistics**: compliance percentage per section, overall, by risk level

### Templates

- Jinja2 templates stored in `templates/reports/`
- Base report template with standard structure
- Tenant-customizable elements: logo, company name, colors, optional sections
- Templates designed with print-friendly CSS (WeasyPrint-compatible)

### PDF Generation

- **WeasyPrint** converts the rendered HTML to PDF
- Supports CSS for headers, footers, page breaks, page numbers
- Generated on-demand (not stored) — reports always reflect current data
- For large reports, generation happens synchronously (acceptable for MVP; can move to background tasks later)

### Excel Generation

- **openpyxl** creates structured Excel workbooks (.xlsx format)
- Multiple worksheets for different report sections:
  - **Summary**: Executive summary, compliance stats, key metrics
  - **Findings**: Non-compliant / partially-compliant responses, grouped by section, with risk levels
  - **Detailed Audit**: Complete checklist with status, evidence, remarks, risk level per item
  - **Statistics**: Charts/tables for compliance by section, by risk level, trend data
- Supports formatting: colors, borders, bold headers, frozen panes
- Generated on-demand (not stored) — reports always reflect current data
- Suitable for data manipulation and further processing in spreadsheet applications

### Report Customization

Per-project report settings stored in `project.settings` (JSONB) or a dedicated table:
- Include/exclude sections
- Custom executive summary text
- Custom recommendations
- Cover page text

---

## 8. Suggested Project Structure

```
themis/
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app factory
│   ├── config.py               # Settings (pydantic-settings)
│   ├── database.py             # Engine, session factory
│   ├── dependencies.py         # FastAPI dependencies (get_db, get_current_user, get_tenant)
│   │
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── tenant.py
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── framework.py        # Framework, Section, Control, ChecklistItem
│   │   ├── project.py          # Project, ProjectMember, ProjectResponse, EvidenceFile
│   │   └── base.py             # Base model with common fields (id, timestamps)
│   │
│   ├── repositories/           # Database access layer
│   │   ├── __init__.py
│   │   ├── base.py             # TenantScopedRepository base class
│   │   ├── user_repo.py
│   │   ├── client_repo.py
│   │   ├── framework_repo.py
│   │   ├── project_repo.py
│   │   └── response_repo.py
│   │
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── client_service.py
│   │   ├── framework_service.py
│   │   ├── project_service.py
│   │   ├── audit_service.py    # Checklist response logic, progress calc
│   │   └── report_service.py   # Report data assembly + generation
│   │
│   ├── routes/                 # FastAPI route handlers
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── clients.py
│   │   ├── frameworks.py
│   │   ├── projects.py
│   │   ├── audit.py
│   │   ├── reports.py
│   │   ├── users.py
│   │   └── settings.py
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth.py             # Session validation, inject current_user
│   │   └── tenant.py           # Inject tenant context
│   │
│   └── utils/
│       ├── __init__.py
│       ├── security.py         # Password hashing, session signing
│       └── pdf.py              # WeasyPrint wrapper
│
├── templates/                  # Jinja2 templates
│   ├── base.html               # Main layout
│   ├── components/             # Reusable UI components (nav, sidebar, cards)
│   ├── auth/
│   ├── dashboard/
│   ├── clients/
│   ├── frameworks/
│   ├── projects/
│   ├── audit/
│   ├── reports/                # Report templates (both preview and PDF)
│   ├── users/
│   ├── settings/
│   └── partials/               # HTMX partial responses
│
├── static/
│   ├── css/
│   │   └── output.css          # Tailwind compiled output
│   ├── js/                     # Alpine.js, HTMX (vendored or CDN)
│   └── uploads/                # Evidence file uploads (dev only; use object storage in prod)
│
├── seeds/                      # Framework seed data
│   ├── pci_dss_v4.json
│   ├── iso_27001.json
│   ├── pdpa.json
│   └── itgc.json
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_projects.py
│   ├── test_audit.py
│   └── test_reports.py
│
├── alembic.ini
├── pyproject.toml
├── tailwind.config.js
├── CLAUDE.md
└── README.md
```

---

## 9. Development Phases / Roadmap

### Phase 1: Foundation (Week 1-2)
- Project setup: FastAPI app, PostgreSQL, Alembic, Tailwind build
- Database models + initial migration
- Base template (layout, nav, sidebar)
- Auth module: login, logout, session management
- Tenant + user models, middleware for tenant context
- Seed a default tenant + admin user

**Deliverable**: Working app shell with login and empty dashboard.

### Phase 2: Core Data Management (Week 3-4)
- Client CRUD (full pages + HTMX interactions)
- Framework engine: models, CRUD, tree display
- Framework seed data: import PCI DSS and one ISO standard
- Framework import/export (JSON)
- User management (admin creates auditors)

**Deliverable**: Can manage clients, browse framework trees, manage users.

### Phase 3: Project & Audit Execution (Week 5-7)
- Project CRUD with client + framework selection
- Project creation triggers checklist snapshot (populate `project_responses`)
- Audit execution view: section tree + checklist items
- Inline response editing (HTMX): status, remarks, risk level
- Evidence file upload
- Progress tracking per section and overall

**Deliverable**: Full audit execution workflow — create project, fill checklist, track progress.

### Phase 4: Reports & Dashboard (Week 8-9)
- Dashboard: project stats, compliance overview
- Report data assembler service
- Report HTML template (executive summary, findings, recommendations)
- PDF generation with WeasyPrint
- Report customization settings

**Deliverable**: Generate and download audit reports as PDF.

### Phase 5: Polish & Hardening (Week 10)
- Role-based access control enforcement across all routes
- Input validation and error handling
- Flash messages / toast notifications
- Responsive design pass (mobile-friendly)
- Basic test suite for critical paths
- Documentation

**Deliverable**: Production-ready MVP.

### Future Phases (Post-MVP)
- Audit trail / activity log
- Email notifications
- Finding remediation tracking
- Multi-framework projects (single project, multiple frameworks)
- Template library for common findings/recommendations
- API tokens for external integrations
- Bulk evidence upload (ZIP)
- AI-assisted recommendations

---

## 10. Key Technical Decisions and Trade-Offs

### 1. Server-Rendered vs SPA
**Decision**: Server-rendered with HTMX
**Reasoning**: Audit workflows are form-heavy and sequential. HTMX provides dynamic updates without the complexity of a JS framework, build tooling, or API serialization layer. The team writes Python, not TypeScript. Trade-off: less flexibility for complex real-time UI (not needed here).

### 2. Session Auth vs JWT
**Decision**: Server-side sessions (cookie-based)
**Reasoning**: No separate frontend that needs token-based auth. Sessions are simpler, revocable, and natural for server-rendered apps. Using `itsdangerous` signed cookies or a session middleware like `starsessions` with DB/Redis backend.

### 3. Shared Schema Multi-Tenancy vs Schema-per-Tenant
**Decision**: Shared schema with `tenant_id` column
**Reasoning**: For MVP with expected <50 tenants, this is far simpler operationally. One migration path, one connection pool. The trade-off is less isolation — a bug in tenant filtering could leak data. Mitigation: repository base class enforces filtering; integration tests verify isolation.

### 4. Framework Snapshot on Project Creation
**Decision**: When a project is created, `project_responses` rows are pre-populated from the framework's checklist items.
**Reasoning**: If a framework is updated after a project starts, the active audit must not change. The snapshot ensures audit integrity. Trade-off: duplicated data, slightly more storage. Worth it for data consistency.

### 5. UUID Primary Keys vs Auto-Increment
**Decision**: UUIDs
**Reasoning**: Avoids sequential ID enumeration (security), simpler data migration between environments, no collision risk. Trade-off: slightly larger, no natural ordering (use `created_at` for ordering).

### 6. PDF Library: WeasyPrint vs Puppeteer/Playwright
**Decision**: WeasyPrint
**Reasoning**: Pure Python, no headless browser dependency, good CSS support for print layouts. Trade-off: CSS support is not 100% browser-equivalent, but sufficient for structured audit reports. Avoids the operational complexity of managing a headless Chrome process.

### 7. File Storage: Local vs Object Storage
**Decision**: Local filesystem for MVP, with abstraction layer for future S3/MinIO migration
**Reasoning**: Simplest to start. Evidence files are stored in `static/uploads/{tenant_id}/{project_id}/`. A `FileStorage` service interface makes it easy to swap to S3 later. Trade-off: not suitable for multi-server deployment without shared filesystem.

### 8. Sync vs Async SQLAlchemy
**Decision**: Synchronous for MVP
**Reasoning**: Simpler debugging, simpler transaction management, no async session complexity. FastAPI runs sync handlers in a threadpool, which is adequate for the expected load. Can migrate to async if performance demands it.

### 9. Framework Data: Self-Referential Sections
**Decision**: `framework_sections` has a `parent_section_id` for nested hierarchy
**Reasoning**: Many frameworks (PCI DSS, ISO) have nested section numbering (1 → 1.1 → 1.1.1). A self-referential table handles arbitrary depth. Trade-off: recursive queries are slightly more complex (use CTE or eager-load with depth limit). In practice, depth rarely exceeds 3 levels.

### 10. No Background Task Queue for MVP
**Decision**: All operations synchronous, including PDF generation
**Reasoning**: Audit reports are bounded in size (hundreds of items, not millions). WeasyPrint renders in seconds. Adding Celery/Redis is unnecessary complexity for MVP. If PDF generation becomes slow for very large audits, add a simple background task later.
