from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.tenant import Tenant
from app.models.user import User
from app.models.project import Project


class AdminTenantRepository:
    def __init__(self, *, db: AsyncSession):
        self.db = db

    async def list_tenants(self) -> list[Tenant]:
        result = await self.db.execute(
            select(Tenant).order_by(Tenant.name)
        )
        return result.scalars().all()

    async def get_tenant_health(self, tenant_id: int) -> dict:
        user_count = await self.db.scalar(
            select(func.count(User.id)).where(User.tenant_id == tenant_id)
        )

        project_count = await self.db.scalar(
            select(func.count(Project.id)).where(Project.tenant_id == tenant_id)
        )

        return {
            "tenant_id": tenant_id,
            "users": user_count or 0,
            "projects": project_count or 0,
        }
