from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate

async def create_tenant(
    *,
    db: AsyncSession,
    tenant_in: TenantCreate
) -> Tenant:
    """
    Create a new tenant record.
    """
    tenant = Tenant(
        name=tenant_in.name
    )

    db.add(tenant)

    try:
        await db.commit()
    except IntegrityError:
        db.rollback()
        raise

    await db.refresh(tenant)
    return tenant


async def get_tenant_by_id(
    *,
    db: AsyncSession,
    tenant_id: int
) -> Tenant | None:
    """
    Fetch a tenant by its primary key.
    """
    
    result = await db.execute(
        select(Tenant).where(Tenant.id == tenant_id)
    )
    return result.scalar_one_or_none()


async def get_tenant_by_name(
    *,    
    db: AsyncSession,
    name: str
) -> Tenant | None:
    """
    Fetch a tenant by its unique name.
    """
    
    result = await db.execute(
        select(Tenant).where(Tenant.name == name)
    )
    return result.scalar_one_or_none()


async def list_tenants(
    *,
    db: AsyncSession
) -> list[Tenant]:
    """
    Return all tenants in the system.
    """
    result = await db.execute(
        select(Tenant).order_by(Tenant.name)
    )
    return result.scalar_one_or_none()
