from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.project import ProjectCreate, ProjectRead
from app.repositories.project import ProjectRepository
from app.api.deps import require_tenant
from app.api.deps.auth import get_current_user
from app.models.user import User
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
    tenant: Tenant = Depends(require_tenant),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a project for the current tenant.
    """
    repo = ProjectRepository(
        db=db,
        tenant=tenant,
        user=current_user,
    )
    return await repo.create(name=project_in.name)
    


@router.get(
    "",
    response_model=list[ProjectRead],
    status_code=status.HTTP_200_OK,
)
async def list_projects(
    tenant: Tenant = Depends(require_tenant),
    db: AsyncSession = Depends(get_db),
):
    """
    List all projects for the current tenant.
    """
    repo = ProjectRepository(db=db, tenant=tenant)
    return await repo.list_all()
