from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.project import ProjectCreate, ProjectRead
from app.repositories.project import create_project_for_tenant
from app.core.tenant_context import get_current_tenant
from app.models.tenant import Tenant
from app.db.session import get_db


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post(
    "",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    project_in: ProjectCreate,
    tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    """
    Create a project for the current tenant.
    """
    return create_project_for_tenant(
        db=db,
        tenant=tenant,
        name=project_in.name,
    )
