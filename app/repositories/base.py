from typing import Type, TypeVar, Generic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.tenant import Tenant

ModelType = TypeVar("ModelType")


class TenantScopedRepository(Generic[ModelType]):
    def __init__(
        self,
        *,
        db: AsyncSession,
        tenant: Tenant,
        model: Type[ModelType],
    ):
        self.db = db
        self.tenant = tenant
        self.model = model

    async def get_by_id(self, id: int) -> ModelType | None:
        result = await self.db.execute(
            select(self.model).where(
                self.model.id == id,
                self.model.tenant_id == self.tenant.id,
            )
        )
        return result.scalar_one_or_none()

    async def list_all(self) -> list[ModelType]:
        result = await self.db.execute(
            select(self.model).where(
                self.model.tenant_id == self.tenant.id
            )
        )
        return result.scalars().all()
