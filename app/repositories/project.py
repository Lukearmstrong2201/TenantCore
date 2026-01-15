from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.project import Project
from app.models.tenant import Tenant

class ProjectRepository:
    def __init__(
        self,
        *,
        db: AsyncSession,
        tenant: Tenant,
    ):
        self.db = db
        self.tenant = tenant

    async def create(self, *, name: str) -> Project:
        """
        Create a project scoped to the current tenant.
        """
        project = Project(
            name=name,
            tenant_id=self.tenant.id,
        )

        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)

        return project

    async def list_all(self) -> list[Project]:
        """
        Return all projects belonging to the current tenant.
        """
        result = await self.db.execute(
            select(Project).where(
                Project.tenant_id == self.tenant.id
            )
        )
        return result.scalars().all()