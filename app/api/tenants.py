from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.schemas.tenant import TenantCreate, TenantRead
from app.core.tenant_context import get_current_tenant
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
    tenant_in: TenantCreate,
    db: Session = Depends(get_db),
):
    """
    Create a tenant and persist it to the database.
    """
    tenant = Tenant(name=tenant_in.name)

    db.add(tenant)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tenant with this name already exists",
        )
    
    db.refresh(tenant)
    return tenant


@router.get(
    "",
    response_model=List[TenantRead],
)
def list_tenants(
    current_tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    """
    Return all tenants.
    Tenant context enforced.
    """

    tenants = db.query(Tenant).order_by(Tenant.id).all()
    return tenants






