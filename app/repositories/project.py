from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.project import Project
from app.models.tenant import Tenant
from app.repositories.base import TenantScopedRepository
from app.models.project_membership import ProjectMembership


class ProjectRepository(TenantScopedRepository[Project]):
    def __init__(
        self,
        *,
        db: AsyncSession,
        tenant: Tenant,
        user: User,
    ):
        super().__init__(
            db=db,
            tenant=tenant,
            model=Project,
        )
        self.user = user

    async def create(self, *, name: str) -> Project:
        """
        Create a project scoped to the current tenant.
        """
        project = Project(
            name=name,
            tenant_id=self.tenant.id,
        )

        self.db.add(project)
        await self.db.flush()

        membership = ProjectMembership(
        tenant_id=self.tenant.id,
        project_id=project.id,
        user_id=self.user.id,
        role="OWNER",
    )

        self.db.add(membership)
        await self.db.commit()
        await self.db.refresh(project)

        return project