from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.auth import get_current_user
from app.api.deps.tenant import get_current_tenant
from app.db.session import get_db

from app.models.user import User
from app.models.tenant import Tenant
from app.schemas.audit_log import AuditLogRead
from app.crud.audit_log import list_audit_logs


router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"],
)


@router.get("", response_model=list[AuditLogRead])
async def get_audit_logs(
    limit: int = Query(50, le=100),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
):
    # Restrict to tenant admins only
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return await list_audit_logs(
        db=db,
        tenant_id=current_tenant.id,
        limit=limit,
        offset=offset,
    )
