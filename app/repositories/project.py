from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.project import Project
from app.models.tenant import Tenant


async def create_project_for_tenant(
    *,
    db: AsyncSession,
    tenant: Tenant,
    name: str,
) -> Project:
    """
    Create a project scoped to a tenant.
    """
    project = Project(
        name=name,
        tenant_id=tenant.id,
    )

    db.add(project)
    await db.flush()
    await db.refresh(project)

    return project


async def get_projects_for_tenant(
    *,
    db: AsyncSession,
    tenant: Tenant,
) -> list[Project]:
    """
    Return all projects belonging to a tenant.
    """
    result = await db.execute(
        select(Project).where(Project.tenant_id == tenant.id)
    )
    return result.scalars().all()