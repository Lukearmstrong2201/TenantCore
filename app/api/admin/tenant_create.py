from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import require_admin
from app.schemas.tenant import TenantCreate, TenantRead
from app.repositories.tenant import create_tenant
from app.models.user import User


router = APIRouter(
    prefix="/admin/tenants",
    tags=["Admin – Tenants"],
)


@router.post(
    "",
    response_model=TenantRead,
    status_code=status.HTTP_201_CREATED,
)
async def admin_create_tenant(
    tenant_in: TenantCreate,
    _: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    try:
        tenant = await create_tenant(db=db, tenant_in=tenant_in)
        await db.commit()
        await db.refresh(tenant)
        return tenant
    except Exception:
        await db.rollback()
        raise
