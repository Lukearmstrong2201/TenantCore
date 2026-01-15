from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.tenant import Tenant


class AdminTenantRepository:
    """
    Repository for system level tenant access.
    ADMIN ONLY.
    """

    def __init__(self, *, db: AsyncSession):
        self.db = db

    async def list_all(self) -> list[Tenant]:
        result = await self.db.execute(
            select(Tenant).order_by(Tenant.name)
        )
        return result.scalars().all()

    async def get_by_id(self, tenant_id: int) -> Tenant | None:
        result = await self.db.execute(
            select(Tenant).where(Tenant.id == tenant_id)
        )
        return result.scalar_one_or_none()
