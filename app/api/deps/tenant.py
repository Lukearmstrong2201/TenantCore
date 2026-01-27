from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.tenant import Tenant
from app.repositories.tenant import get_tenant_by_id



async def get_current_tenant(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Tenant:
    """
    Resolve the tenant for the current authenticated user.
    """
    if not current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not associated with a tenant",
        )

    tenant = await get_tenant_by_id(
        db=db,
        tenant_id=current_user.tenant_id,
    )

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    return tenant


async def require_tenant(
    tenant: Tenant = Depends(get_current_tenant),
) -> Tenant:
    """
    Enforce that a valid tenant context exists.
    """
    return tenant