from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.user import User
from app.repositories.admin_tenant import AdminTenantRepository
from app.schemas.tenant import TenantRead

router = APIRouter(
    prefix="/admin/tenants",
    tags=["Admin – Tenants"],
)


@router.get(
    "",
    response_model=list[TenantRead],
)
async def list_tenants(
    _: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    repo = AdminTenantRepository(db=db)
    return await repo.list_all()


@router.get(
    "/{tenant_id}",
    response_model=TenantRead,
)
async def get_tenant(
    tenant_id: int,
    _: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    repo = AdminTenantRepository(db=db)
    tenant = await repo.get_by_id(tenant_id)

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    return tenant
