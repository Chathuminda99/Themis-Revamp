# Themis — Compliance & Risk Management Platform

## Overview
Themis is a web-based compliance and risk management platform designed to streamline security assessments, compliance tracking, and evidence management.

## Phase 1: Foundation
This phase establishes the project foundation with authentication, database models, and a dark-themed dashboard interface.

## Prerequisites
- Python 3.14.2+
- Node.js v22.22.0+
- PostgreSQL 18.2+
- uv (Python package manager)

## Setup Instructions

### 1. Create Database
```bash
createdb themis_dev
```

### 2. Clone and Navigate to Project
```bash
cd /home/lasitha/Documents/Projects/Themis-Revamp
```

### 3. Create Python Virtual Environment
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 4. Install Python Dependencies
```bash
uv pip install -e ".[dev]"
```

### 5. Create `.env` File
```bash
cp .env.example .env
# Edit .env and set DATABASE_URL correctly
```

### 6. Install Node Dependencies and Build CSS
```bash
npm install
npm run build:css
```

### 7. Run Database Migrations
```bash
alembic upgrade head
```

### 8. Seed Default Data
```bash
python seeds/seed.py
```

### 9. Start Development Server
```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000` in your browser.

## Default Login Credentials
- **Email**: `admin@themis.local`
- **Password**: `admin123`

## Development Workflow

### Watch Tailwind CSS for Changes
In another terminal:
```bash
npm run watch:css
```

### Create Database Migration
```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Project Structure
```
.
├── app/                      # Application code
│   ├── models/              # SQLAlchemy ORM models
│   ├── routes/              # FastAPI route handlers
│   ├── middleware/          # Custom middleware
│   ├── services/            # Business logic
│   ├── utils/               # Utilities (security, etc.)
│   ├── config.py            # Configuration
│   ├── database.py          # Database setup
│   ├── dependencies.py      # Dependency injection
│   └── main.py              # Application factory
├── alembic/                 # Database migrations
├── seeds/                   # Seed scripts
├── static/                  # Static files (CSS, JS)
├── templates/               # Jinja2 HTML templates
├── pyproject.toml           # Python project config
├── package.json             # Node.js dependencies
└── README.md                # This file
```

## Environment Variables
See `.env.example` for all available configuration options.

## License
MIT
