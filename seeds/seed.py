#!/usr/bin/env python
"""Seed script to populate initial data."""

import sys
import uuid
from sqlalchemy.orm import Session

# Add app directory to path
sys.path.insert(0, "/home/lasitha/Documents/Projects/Themis-Revamp")

from app.database import SessionLocal, engine
from app.models import BaseModel, Tenant, User, UserRole
from app.utils.security import hash_password


def seed_database():
    """Create default tenant and admin user."""
    # Create all tables
    BaseModel.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    try:
        # Check if default tenant exists
        default_tenant = (
            db.query(Tenant).filter(Tenant.slug == "demo-company").first()
        )

        if default_tenant:
            print("✓ Default tenant already exists")
            tenant_id = default_tenant.id
        else:
            # Create default tenant
            tenant_id = uuid.uuid4()
            tenant = Tenant(
                id=tenant_id,
                name="Demo Company",
                slug="demo-company",
                logo_url=None,
                settings={},
            )
            db.add(tenant)
            db.commit()
            print("✓ Created default tenant: Demo Company")

        # Check if admin user exists
        admin_user = db.query(User).filter(User.email == "admin@themis.local").first()

        if admin_user:
            print("✓ Admin user already exists")
        else:
            # Create admin user
            admin_user = User(
                id=uuid.uuid4(),
                tenant_id=tenant_id,
                email="admin@themis.local",
                password_hash=hash_password("admin123"),
                full_name="Administrator",
                role=UserRole.ADMIN,
                is_active=True,
            )
            db.add(admin_user)
            db.commit()
            print("✓ Created admin user: admin@themis.local / admin123")

        print("\n✅ Database seeded successfully!")

    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
