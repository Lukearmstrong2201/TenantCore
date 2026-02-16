from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.project import require_project_access
from app.db.session import get_db
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
):
    repo = TaskRepository(db)
    return await repo.create(
        project_id=project.id,
        title=payload.title,
        description=payload.description,
    )


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
):
    repo = TaskRepository(db)
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
):
    repo = TaskRepository(db)
    task = await repo.get(project.id, task_id)

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
):
    repo = TaskRepository(db)
    task = await repo.get(project.id, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await repo.delete(task)




