from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate

def create_tenant(db: Session, tenant_in: TenantCreate) -> Tenant:
    """
    Create a new tenant record in the database.

    This function:
    - Accepts a SQLAlchemy DB session
    - Accepts validated input data (TenantCreate schema)
    - Translates schema -> SQLAlchemy model
    - Persists it to Postgres
    - Returns the created Tenant model
    """
    tenant = Tenant(
        name=tenant_in.name
    )

    db.add(tenant)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(tenant)
    return tenant


def get_tenant_by_id(db: Session, tenant_id: int) -> Tenant | None:
    """
    Fetch a tenant by its primary key.

    Returns:
    - Tenant if found
    - None if no record exists
    """
    
    return (
        db.query(Tenant)
        .filter(Tenant.id == tenant_id)
        .first()
    )


def get_tenant_by_name(db: Session, name: str) -> Tenant | None:
    """
    Fetch a tenant by its unique name.

    Useful for:
    - Duplicate checks
    - Lookup by human-readable identifier
    """
    
    return (
        db.query(Tenant)
        .filter(Tenant.name == name)
        .first()
    )


def list_tenants(db: Session) -> list[Tenant]:
    """
    Return all tenants in the system.

    Notes:
    - Returns raw SQLAlchemy models
    - Ordering is done at the DB level
    """
    
    return db.query(Tenant).order_by(Tenant.name).all()


def get_all_tenants(db: Session) -> list[Tenant]:
    """
    Fetch all tenants from the database.
    """
    result = db.execute(select(Tenant))
    return result.scalars().all()