from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.tenant import TenantCreate, TenantRead
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
def create_tenant(
    tenant: TenantCreate,
    db: Session = Depends(get_db),
):
    """
    Create a tenant and persist it to the database.
    """
    db_tenant = Tenant(name=tenant.name)

    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)

    return db_tenant