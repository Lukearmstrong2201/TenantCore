from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.tenant import Tenant
from app.repositories.base import TenantScopedRepository

class ProjectRepository(TenantScopedRepository[Project]):
    def __init__(
        self,
        *,
        db: AsyncSession,
        tenant: Tenant,
    ):
        super().__init__(
            db=db,
            tenant=tenant,
            model=Project,
        )

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