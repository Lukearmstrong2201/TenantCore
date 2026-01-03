from sqlalchemy.orm import Session
from typing import Type, TypeVar

from app.models.mixins import TenantScopedMixin

ModelType = TypeVar("ModelType")


def tenant_query(
    db: Session,
    model: Type[ModelType],
    tenant_id: int,
):
    """
    Returns a query scoped to the given tenant.

    Prevents cross-tenant data access.
    """
    if not issubclass(model, TenantScopedMixin):
        raise ValueError("Model is not tenant-scoped")

    return db.query(model).filter(model.tenant_id == tenant_id)
