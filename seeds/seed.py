#!/usr/bin/env python
"""Seed script to populate initial data."""

import sys
import uuid
from sqlalchemy.orm import Session

# Add app directory to path
sys.path.insert(0, "/home/lasitha/Documents/Projects/Themis-Revamp")

from app.database import SessionLocal, engine
from app.models import (
    BaseModel,
    Tenant,
    User,
    UserRole,
    Client,
    Framework,
    FrameworkSection,
    FrameworkControl,
    ChecklistItem,
    Project,
    ProjectStatus,
)
from app.utils.security import hash_password


def seed_database():
    """Create default tenant, admin user, clients, frameworks, and projects."""
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

        # Check if clients already exist
        existing_clients = db.query(Client).filter(
            Client.tenant_id == tenant_id
        ).count()

        if existing_clients == 0:
            # Create clients
            acme_id = uuid.uuid4()
            acme = Client(
                id=acme_id,
                tenant_id=tenant_id,
                name="Acme Corporation",
                industry="Technology",
                contact_name="John Doe",
                contact_email="john.doe@acme.com",
                notes="Leading tech company",
            )

            beta_id = uuid.uuid4()
            beta = Client(
                id=beta_id,
                tenant_id=tenant_id,
                name="Beta Ltd",
                industry="Finance",
                contact_name="Jane Smith",
                contact_email="jane.smith@beta.com",
                notes="Financial services provider",
            )

            db.add_all([acme, beta])
            db.commit()
            print("✓ Created 2 clients: Acme Corporation, Beta Ltd")
        else:
            acme = db.query(Client).filter(
                Client.tenant_id == tenant_id,
                Client.name == "Acme Corporation"
            ).first()
            beta = db.query(Client).filter(
                Client.tenant_id == tenant_id,
                Client.name == "Beta Ltd"
            ).first()
            acme_id = acme.id if acme else None
            beta_id = beta.id if beta else None
            print("✓ Clients already exist")

        # Check if frameworks exist
        existing_frameworks = db.query(Framework).filter(
            Framework.tenant_id == tenant_id
        ).count()

        if existing_frameworks == 0:
            # Create ISO 27001 framework
            iso_id = uuid.uuid4()
            iso = Framework(
                id=iso_id,
                tenant_id=tenant_id,
                name="ISO 27001:2022",
                description="Information security management standard",
                version="2022",
            )
            db.add(iso)
            db.flush()

            # Create ISO 27001 sections
            iso_a5_id = uuid.uuid4()
            iso_a5 = FrameworkSection(
                id=iso_a5_id,
                framework_id=iso_id,
                parent_section_id=None,
                name="A.5 Organizational Controls",
                description="Controls for organization-wide policies",
                order=1,
            )
            db.add(iso_a5)
            db.flush()

            iso_a8_id = uuid.uuid4()
            iso_a8 = FrameworkSection(
                id=iso_a8_id,
                framework_id=iso_id,
                parent_section_id=None,
                name="A.8 Technological Controls",
                description="Technical security controls",
                order=2,
            )
            db.add(iso_a8)
            db.flush()

            # Add controls to ISO A.5
            iso_a5_1 = FrameworkControl(
                id=uuid.uuid4(),
                framework_section_id=iso_a5_id,
                control_id="A.5.1",
                name="Policies for information security",
                description="Information security policies established",
            )
            iso_a5_2 = FrameworkControl(
                id=uuid.uuid4(),
                framework_section_id=iso_a5_id,
                control_id="A.5.2",
                name="Information security roles and responsibilities",
                description="Clear roles and responsibilities defined",
            )
            db.add_all([iso_a5_1, iso_a5_2])
            db.flush()

            # Add controls to ISO A.8
            iso_a8_1 = FrameworkControl(
                id=uuid.uuid4(),
                framework_section_id=iso_a8_id,
                control_id="A.8.1",
                name="User endpoint devices",
                description="Endpoint device security implemented",
            )
            db.add(iso_a8_1)
            db.flush()

            # Add checklist items
            db.add(ChecklistItem(
                id=uuid.uuid4(),
                framework_control_id=iso_a5_1.id,
                description="Information security policy document reviewed",
                is_mandatory=True,
            ))
            db.add(ChecklistItem(
                id=uuid.uuid4(),
                framework_control_id=iso_a5_2.id,
                description="CISO appointed and documented",
                is_mandatory=True,
            ))

            db.commit()
            iso_framework_id = iso_id
            print("✓ Created ISO 27001:2022 framework with sections and controls")

            # Create SOC 2 framework
            soc2_id = uuid.uuid4()
            soc2 = Framework(
                id=soc2_id,
                tenant_id=tenant_id,
                name="SOC 2 Type II",
                description="System and Organization Controls framework",
                version="2023",
            )
            db.add(soc2)
            db.flush()

            # Create SOC 2 sections
            soc2_cc1_id = uuid.uuid4()
            soc2_cc1 = FrameworkSection(
                id=soc2_cc1_id,
                framework_id=soc2_id,
                parent_section_id=None,
                name="CC1 Control Environment",
                description="Foundation for security controls",
                order=1,
            )
            db.add(soc2_cc1)
            db.flush()

            # Add controls to SOC 2
            soc2_cc1_1 = FrameworkControl(
                id=uuid.uuid4(),
                framework_section_id=soc2_cc1_id,
                control_id="CC1.1",
                name="Demonstrates Commitment to Integrity",
                description="COSO Principle 1 implementation",
            )
            db.add(soc2_cc1_1)
            db.commit()
            soc2_framework_id = soc2_id
            print("✓ Created SOC 2 Type II framework with sections and controls")
        else:
            iso_framework = db.query(Framework).filter(
                Framework.tenant_id == tenant_id,
                Framework.name == "ISO 27001:2022"
            ).first()
            soc2_framework = db.query(Framework).filter(
                Framework.tenant_id == tenant_id,
                Framework.name == "SOC 2 Type II"
            ).first()
            iso_framework_id = iso_framework.id if iso_framework else None
            soc2_framework_id = soc2_framework.id if soc2_framework else None
            print("✓ Frameworks already exist")

        # Check if projects exist
        existing_projects = db.query(Project).filter(
            Project.tenant_id == tenant_id
        ).count()

        if existing_projects == 0 and acme_id and iso_framework_id:
            # Create projects
            project1 = Project(
                id=uuid.uuid4(),
                tenant_id=tenant_id,
                client_id=acme_id,
                framework_id=iso_framework_id,
                name="Acme ISO 27001 Assessment",
                description="ISO 27001 compliance assessment for Acme Corp",
                status=ProjectStatus.IN_PROGRESS,
            )

            if beta_id and soc2_framework_id:
                project2 = Project(
                    id=uuid.uuid4(),
                    tenant_id=tenant_id,
                    client_id=beta_id,
                    framework_id=soc2_framework_id,
                    name="Beta SOC 2 Readiness",
                    description="SOC 2 Type II readiness assessment for Beta Ltd",
                    status=ProjectStatus.DRAFT,
                )
                db.add_all([project1, project2])
            else:
                db.add(project1)

            db.commit()
            print("✓ Created projects")
        else:
            print("✓ Projects already exist")

        print("\n✅ Database seeded successfully!")

    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
