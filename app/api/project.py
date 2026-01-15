from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.project import ProjectCreate, ProjectRead
from app.repositories.project import create_project_for_tenant, get_projects_for_tenant
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
async def create_project(
    project_in: ProjectCreate,
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a project for the current tenant.
    """
    return await create_project_for_tenant(
        db=db,
        tenant=tenant,
        name=project_in.name,
    )


@router.get(
    "",
    response_model=list[ProjectRead],
    status_code=status.HTTP_200_OK,
)
async def list_projects(
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    """
    List all projects for the current tenant.
    """
    return await get_projects_for_tenant(
        db=db,
        tenant=tenant,
    )
