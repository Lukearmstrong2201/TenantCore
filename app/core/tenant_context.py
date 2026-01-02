from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.tenant import Tenant


def get_current_tenant(
    tenant_id: int = Header(..., alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
) -> Tenant:
    """
    Resolve the current tenant from the X-Tenant-ID header.

    This dependency:
    - Enforces tenant presence on the request
    - Ensures the tenant exists
    - Provides the Tenant object to downstream handlers
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    return tenant
