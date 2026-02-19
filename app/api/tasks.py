from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.project import require_project_access
from app.api.deps.auth import get_current_user
from app.api.deps.tenant import get_current_tenant
from app.db.session import get_db

from app.models.user import User
from app.models.tenant import Tenant
from app.models.project_membership import ProjectRole

from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskRead


router = APIRouter(
    prefix="/projects/{project_id}/tasks",
    tags=["Tasks"],
)


@router.post("", response_model=TaskRead)
async def create_task(
    payload: TaskCreate,
    project=Depends(
        require_project_access(
            allowed_roles={
                ProjectRole.MEMBER,
                ProjectRole.ADMIN,
                ProjectRole.OWNER,
            }
        )
    ),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
):
    repo = TaskRepository(db=db, tenant=current_tenant, user=current_user)

    try:
        task = await repo.create(
            project_id=project.id,
            title=payload.title,
            description=payload.description,
        )
        await db.commit()
        await db.refresh(task)
        return task
    except Exception:
        await db.rollback()
        raise



@router.get("", response_model=list[TaskRead])
async def list_tasks(
    project=Depends(
        require_project_access(
            allowed_roles={
                ProjectRole.VIEWER,
                ProjectRole.MEMBER,
                ProjectRole.ADMIN,
                ProjectRole.OWNER,
            }
        )
    ),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
):
    repo = TaskRepository(
        db=db,
        tenant=current_tenant,
        user=current_user,
    )

    return await repo.list(project_id=project.id)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: int,
    project=Depends(
        require_project_access(
            allowed_roles={
                ProjectRole.VIEWER,
                ProjectRole.MEMBER,
                ProjectRole.ADMIN,
                ProjectRole.OWNER,
            }
        )
    ),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
):
    repo = TaskRepository(
        db=db,
        tenant=current_tenant,
        user=current_user,
    )

    task = await repo.get(project_id=project.id, task_id=task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    project=Depends(
        require_project_access(
            allowed_roles={
                ProjectRole.ADMIN,
                ProjectRole.OWNER,
            }
        )
    ),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
):
    repo = TaskRepository(db=db, tenant=current_tenant, user=current_user)

    task = await repo.get(project_id=project.id, task_id=task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        await repo.delete(task=task)
        await db.commit()
    except Exception:
        await db.rollback()
        raise




