from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.project import ProjectCreate, ProjectRead
from app.repositories.project import ProjectRepository
from app.api.deps import require_tenant
from app.api.deps.auth import get_current_user
from app.api.deps.project import require_project_access
from app.schemas.project_membership import ProjectMemberAdd, ProjectMemberUpdate
from app.repositories.project_membership import ProjectMembershipRepository
from app.models.project_membership import ProjectRole
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
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    List all projects for the current tenant.
    """
    repo = ProjectRepository(
        db=db, 
        tenant=tenant, 
        user=current_user,
    )
    return await repo.list_for_user()


@router.get(
    "/{project_id}",
    response_model=ProjectRead,
)
async def get_project(
    project=Depends(
        require_project_access(
            allowed_roles={
                ProjectRole.OWNER,
                ProjectRole.ADMIN,
                ProjectRole.MEMBER,
                ProjectRole.VIEWER,
            }
        )
    ),
):
    return project


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project=Depends(
        require_project_access(
            allowed_roles={ProjectRole.OWNER}
        )
    ),
):
    # deletion logic coming later
    pass


@router.post(
    "/{project_id}/members",
    status_code=status.HTTP_201_CREATED,
)
async def add_project_member(
    payload: ProjectMemberAdd,
    project=Depends(
        require_project_access(
            allowed_roles={ProjectRole.OWNER, ProjectRole.ADMIN}
        )
    ),
    tenant: Tenant = Depends(require_tenant),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Add member to project.
    """
    repo = ProjectMembershipRepository(
        db=db,
        tenant=tenant,
        actor=current_user,
    )

    return await repo.add_member(
        project_id=project.id,
        user_id=payload.user_id,
        role=payload.role,
    )



@router.patch(
    "/{project_id}/members/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_project_member(
    user_id: int,
    payload: ProjectMemberUpdate,
    project=Depends(
        require_project_access(
            allowed_roles={ProjectRole.OWNER}
        )
    ),
    tenant: Tenant = Depends(require_tenant),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Update member role.
    """
    repo = ProjectMembershipRepository(
        db=db,
        tenant=tenant,
        actor=current_user,
    )

    await repo.update_role(
        project_id=project.id,
        user_id=user_id,
        role=payload.role,
    )


@router.delete(
    "/{project_id}/members/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_project_member(
    user_id: int,
    project=Depends(
        require_project_access(
            allowed_roles={ProjectRole.OWNER}
        )
    ),
    tenant: Tenant = Depends(require_tenant),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ProjectMembershipRepository(
        db=db,
        tenant=tenant,
        actor=current_user,
    )

    if await repo.owner_count(project.id) <= 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project must have at least one owner",
        )

    await repo.remove_member(
        project_id=project.id,
        user_id=user_id,
    )
