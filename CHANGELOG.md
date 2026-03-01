# Changelog

All notable changes to Themis Revamp are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and versioning follows [SemVer](https://semver.org/).

---

## [Unreleased]

---

## [0.5.10] — 2026-03-01

### Added
- Persist expanded sidebar sections and active control to `localStorage` so a page refresh fully restores the previous view state

### Changed
- Observations area widened from 2/3 to 3/4 of the form grid (`xl:grid-cols-4`, `xl:col-span-3`)
- Control Metadata and Audit Trail sidebar cards compacted (smaller padding, tighter labels)

### Fixed
- Stale `select.value` reference in `addObservation()` that caused a JS runtime error

---

## [0.5.9] — 2026-03-01

### Added
- Checkpoint and Observations toolbar unified into a single `sticky top-4` wrapper so both freeze during scroll
- `{ once: true }` scroll listener on `#control-details` container to close observation picker dropdown on scroll

### Fixed
- Observation picker dropdown invisible after toolbar restructure (caused by `backdrop-filter` creating a new containing block for `position: fixed` descendants)
- Dropdown not closing when the inner overflow scroll container scrolled (was only listening to `window` scroll)
- Uniform `p-6` padding on Requirements and Testing Procedures content areas

---

## [0.5.8] — 2026-02-28

### Added
- Collapsible Requirements and Testing Procedures panels with smooth transitions
- Sticky pinned Checkpoint panel with purple accent and expand/collapse toggle
- Multi-line observation dropdown labels — no more 60-character truncation (Antigravity #4)
- Fixed-position observation picker dropdown anchored via `getBoundingClientRect()`, preventing clipping by `overflow-hidden` parents (Antigravity #5)

### Fixed
- Observations empty state constrained to table width
- Dotted drop-zone style for the empty observations state (Antigravity #2)
- Sticky Save & Continue / Cancel bar in control detail (Antigravity #1)
- Read More / Show Less toggle for long Requirements and Testing Procedures (Antigravity #3)

---

## [0.5.7] — 2026-02-27

### Fixed
- Dashboard empty state overflow and layout issues

---

## [0.5.6] — 2026-02-27

### Added
- Empty state for dashboard when no active projects exist

---

## [0.5.5] — 2026-02-26

### Fixed
- Dashboard project cards now show real progress percentage instead of hardcoded 0%

---

## [0.5.4] — 2026-02-26

### Added
- Login page redesigned to match the current design system

---

## [0.5.3] — 2026-02-25

### Fixed
- Admin controls pages aligned to design system (removed legacy `gray-*` classes)

---

## [0.5.2] — 2026-02-25

### Added
- Frameworks detail page redesigned to match design system

---

## [0.5.1] — 2026-02-24

### Fixed
- Version badge visibility (`text-[10px]` now compiled, dark mode color corrected)
- Removed excessive `max-width` constraints from Clients and Dashboard pages

---

## [0.5.0] — 2026-02-24

### Added
- Version badge in sidebar footer
- Out-of-band tree icon updates via HTMX after control response save
- Frameworks list page redesigned to match design system (removed legacy `gray-*` classes)
- Sidebar collapse chevron flips direction correctly when open/closed

---

## [0.4.0] — 2026-02-20

### Added
- Unified dropdown styling across all templates using CSS variable design system
- Material Symbols icons throughout the application

### Changed
- Global dropdown refactoring: modern visual hierarchy, consistent hover/active states

---

## [0.3.0] — 2026-02-15

### Added
- Scalable observations system with per-observation evidence management
- Control detail page: requirements, testing procedures, checkpoints display
- Collapsible sidebar with toggle
- PCI DSS framework seed data with assessment checklists
- Control response management (status: `in_progress`, `approved`, `rejected`, `not_applicable`)

### Changed
- Assessment scenarios integrated directly into control detail view

---

## [0.2.0] — 2026-02-10

### Added
- Phase 2: Repositories, CRUD routes, HTMX modals, extended seed data
- Clients, Frameworks, Projects full CRUD with filter/search
- HTMX-powered modals using Alpine.js `$store.modal` pattern
- Client search autocomplete with debounce
- Dashboard stats from real data

---

## [0.1.0] — 2026-02-05

### Added
- Phase 1: FastAPI foundation, SQLAlchemy models, Alembic migrations
- Session authentication with HTTP-only cookies
- Multi-tenancy middleware
- Tailwind CSS design system with dark mode support
- Base templates, sidebar navigation, dashboard skeleton
