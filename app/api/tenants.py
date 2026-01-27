from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from typing import List

from app.repositories.tenant import get_tenant_by_id
from app.schemas.tenant import TenantCreate, TenantRead
from app.api.deps import get_current_tenant
from app.models.tenant import Tenant
from app.db.session import get_db


router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"],
)


@router.post(
    "",
    response_model=TenantRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_tenant(
    tenant_in: TenantCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a tenant and persist it to the database.
    """
    tenant = Tenant(name=tenant_in.name)
    db.add(tenant)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tenant with this name already exists",
        )
    
    await db.refresh(tenant)
    return tenant


@router.get(
    "",
    response_model=List[TenantRead],
)
async def list_tenants(
    current_tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    """
    Return all tenants.
    Tenant context enforced.
    """

    result = await db.execute(
        select(Tenant).order_by(Tenant.id)
    )
    return result.scalars().all()






