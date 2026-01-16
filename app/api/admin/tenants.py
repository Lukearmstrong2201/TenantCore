from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import require_admin
from app.models.user import User
from app.repositories.admin.tenant import AdminTenantRepository


router = APIRouter(
    prefix="/admin/tenants",
    tags=["Admin – Tenants"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def list_tenants(
    _: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    repo = AdminTenantRepository(db=db)
    return await repo.list_tenants()


@router.get(
    "/{tenant_id}/health",
    status_code=status.HTTP_200_OK,
)
async def tenant_health(
    tenant_id: int,
    _: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    repo = AdminTenantRepository(db=db)
    return await repo.get_tenant_health(tenant_id)
