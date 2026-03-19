"""update project and response status enums

Revision ID: b3c4d5e6f7a8
Revises: a1b2c3d4e5f6
Create Date: 2026-03-19 00:00:00.000000

- projectstatus: add NOT_STARTED, remove ARCHIVED → final: NOT_STARTED, DRAFT, IN_PROGRESS, COMPLETED
- responsestatus: add COMPLIED, NOT_COMPLIED, remove SUBMITTED/APPROVED/REJECTED/IN_PROGRESS
  → final: NOT_STARTED, DRAFT, COMPLIED, NOT_COMPLIED
"""
from alembic import op


# revision identifiers
revision = 'b3c4d5e6f7a8'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade():
    # ================================================================
    # 1. projectstatus: NOT_STARTED, DRAFT, IN_PROGRESS, COMPLETED
    # ================================================================

    # Add NOT_STARTED value — requires committed transaction
    op.execute("COMMIT")
    op.execute("ALTER TYPE projectstatus ADD VALUE IF NOT EXISTS 'NOT_STARTED' BEFORE 'DRAFT'")
    op.execute("BEGIN")

    # Migrate ARCHIVED → NOT_STARTED
    op.execute("UPDATE projects SET status = 'NOT_STARTED'::projectstatus WHERE status::text = 'ARCHIVED'")
    op.execute("COMMIT")
    op.execute("BEGIN")

    # Recreate enum without ARCHIVED
    op.execute("CREATE TYPE projectstatus_new AS ENUM ('NOT_STARTED', 'DRAFT', 'IN_PROGRESS', 'COMPLETED')")
    op.execute(
        "ALTER TABLE projects ALTER COLUMN status TYPE projectstatus_new "
        "USING status::text::projectstatus_new"
    )
    op.execute("DROP TYPE projectstatus")
    op.execute("ALTER TYPE projectstatus_new RENAME TO projectstatus")

    # ================================================================
    # 2. responsestatus: NOT_STARTED, DRAFT, COMPLIED, NOT_COMPLIED
    # ================================================================

    # Add new values — requires committed transaction
    op.execute("COMMIT")
    op.execute("ALTER TYPE responsestatus ADD VALUE IF NOT EXISTS 'COMPLIED'")
    op.execute("ALTER TYPE responsestatus ADD VALUE IF NOT EXISTS 'NOT_COMPLIED'")
    op.execute("BEGIN")

    # Migrate old values
    op.execute(
        "UPDATE project_responses SET status = 'DRAFT'::responsestatus "
        "WHERE status::text IN ('IN_PROGRESS', 'SUBMITTED')"
    )
    op.execute(
        "UPDATE project_responses SET status = 'COMPLIED'::responsestatus "
        "WHERE status::text = 'APPROVED'"
    )
    op.execute(
        "UPDATE project_responses SET status = 'NOT_COMPLIED'::responsestatus "
        "WHERE status::text = 'REJECTED'"
    )
    op.execute("COMMIT")
    op.execute("BEGIN")

    # Recreate enum without old values
    op.execute(
        "CREATE TYPE responsestatus_new AS ENUM ('NOT_STARTED', 'DRAFT', 'COMPLIED', 'NOT_COMPLIED')"
    )
    op.execute(
        "ALTER TABLE project_responses ALTER COLUMN status TYPE responsestatus_new "
        "USING status::text::responsestatus_new"
    )
    op.execute("DROP TYPE responsestatus")
    op.execute("ALTER TYPE responsestatus_new RENAME TO responsestatus")


def downgrade():
    # Restore projectstatus with ARCHIVED
    op.execute("COMMIT")
    op.execute("ALTER TYPE projectstatus ADD VALUE IF NOT EXISTS 'ARCHIVED'")
    op.execute("BEGIN")
    op.execute("CREATE TYPE projectstatus_old AS ENUM ('DRAFT', 'IN_PROGRESS', 'COMPLETED', 'ARCHIVED')")
    op.execute(
        "ALTER TABLE projects ALTER COLUMN status TYPE projectstatus_old "
        "USING CASE WHEN status::text = 'NOT_STARTED' THEN 'DRAFT' ELSE status::text END::projectstatus_old"
    )
    op.execute("DROP TYPE projectstatus")
    op.execute("ALTER TYPE projectstatus_old RENAME TO projectstatus")

    # Restore responsestatus with old values
    op.execute("COMMIT")
    op.execute("ALTER TYPE responsestatus ADD VALUE IF NOT EXISTS 'SUBMITTED'")
    op.execute("ALTER TYPE responsestatus ADD VALUE IF NOT EXISTS 'APPROVED'")
    op.execute("ALTER TYPE responsestatus ADD VALUE IF NOT EXISTS 'REJECTED'")
    op.execute("ALTER TYPE responsestatus ADD VALUE IF NOT EXISTS 'IN_PROGRESS'")
    op.execute("BEGIN")
    op.execute(
        "CREATE TYPE responsestatus_old AS ENUM "
        "('NOT_STARTED', 'IN_PROGRESS', 'SUBMITTED', 'APPROVED', 'REJECTED', 'DRAFT')"
    )
    op.execute(
        "ALTER TABLE project_responses ALTER COLUMN status TYPE responsestatus_old "
        "USING CASE "
        "  WHEN status::text = 'COMPLIED' THEN 'APPROVED' "
        "  WHEN status::text = 'NOT_COMPLIED' THEN 'REJECTED' "
        "  ELSE status::text "
        "END::responsestatus_old"
    )
    op.execute("DROP TYPE responsestatus")
    op.execute("ALTER TYPE responsestatus_old RENAME TO responsestatus")
