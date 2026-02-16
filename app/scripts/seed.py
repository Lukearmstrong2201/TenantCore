import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models import Tenant, User, Project, ProjectMembership, Task
from app.core.security import hash_password
from app.models.project_membership import ProjectRole  

TEST_PASSWORD = "test123"

async def seed():
    async with AsyncSessionLocal() as session: 

        # ------------------------
        # Create Tenants
        # ------------------------
        acme = Tenant(name="Acme Corp")
        beta = Tenant(name="Beta Ltd")

        session.add_all([acme, beta])
        await session.flush() 

        # ------------------------
        # Create Users
        # ------------------------
        users = [
            # Acme
            User(
                email="admin@acme.com",
                hashed_password=hash_password(TEST_PASSWORD),
                tenant_id=acme.id,
                is_admin=True,
            ),
            User(
                email="user1@acme.com",
                hashed_password=hash_password(TEST_PASSWORD),
                tenant_id=acme.id,
            ),
            User(
                email="user2@acme.com",
                hashed_password=hash_password(TEST_PASSWORD),
                tenant_id=acme.id,
            ),

            # Beta
            User(
                email="admin@beta.com",
                hashed_password=hash_password(TEST_PASSWORD),
                tenant_id=beta.id,
                is_admin=True,
            ),
            User(
                email="user1@beta.com",
                hashed_password=hash_password(TEST_PASSWORD),
                tenant_id=beta.id,
            ),
        ]

        session.add_all(users)
        await session.flush()

        # ------------------------
        # Create Projects
        # ------------------------
        website = Project(name="Website Redesign", tenant_id=acme.id)
        mobile = Project(name="Mobile App", tenant_id=acme.id)
        crm = Project(name="Internal CRM", tenant_id=beta.id)

        session.add_all([website, mobile, crm])
        await session.flush()

        # ------------------------
        # Project Memberships
        # ------------------------
        memberships = [
    # Acme
    ProjectMembership(
        user_id=users[0].id,
        project_id=website.id,
        role=ProjectRole.OWNER,
        tenant_id=acme.id,
    ),
    ProjectMembership(
        user_id=users[1].id,
        project_id=website.id,
        role=ProjectRole.MEMBER,
        tenant_id=acme.id,
    ),
    ProjectMembership(
        user_id=users[2].id,
        project_id=website.id,
        role=ProjectRole.MEMBER,
        tenant_id=acme.id,
    ),

    ProjectMembership(
        user_id=users[0].id,
        project_id=mobile.id,
        role=ProjectRole.OWNER,
        tenant_id=acme.id,
    ),
    ProjectMembership(
        user_id=users[1].id,
        project_id=mobile.id,
        role=ProjectRole.MEMBER,
        tenant_id=acme.id,
    ),

    # Beta
    ProjectMembership(
        user_id=users[3].id,
        project_id=crm.id,
        role=ProjectRole.OWNER,
        tenant_id=beta.id,
    ),
    ProjectMembership(
        user_id=users[4].id,
        project_id=crm.id,
        role=ProjectRole.MEMBER,
        tenant_id=beta.id,
    ),
]

        session.add_all(memberships)
        await session.flush()

        # ------------------------
        # Tasks
        # ------------------------
        tasks = [
            Task(title="Setup homepage layout", project_id=website.id),
            Task(title="Implement login API", project_id=website.id),
            Task(title="Fix navbar bug", project_id=website.id),

            Task(title="Create onboarding screen", project_id=mobile.id),
            Task(title="Add push notifications", project_id=mobile.id),

            Task(title="Design database schema", project_id=crm.id),
        ]

        session.add_all(tasks)

        await session.commit()

    print("✅ Database seeded successfully.")

if __name__ == "__main__":
    asyncio.run(seed())
