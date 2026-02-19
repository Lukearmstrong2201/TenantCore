from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.audit_log import create_audit_log
from app.models.audit_action import AuditAction
from app.models.task import Task
from app.models.tenant import Tenant
from app.models.user import User


class TaskRepository:
    def __init__(
        self,
        *,
        db: AsyncSession,
        tenant: Tenant,
        user: User,
    ):
        self.db = db
        self.tenant = tenant
        self.user = user

    async def create(
        self,
        *,
        project_id: int,
        title: str,
        description: str | None,
    ) -> Task:
        task = Task(
            project_id=project_id,
            title=title,
            description=description,
        )

        self.db.add(task)

        # Needed if ID is required before commit
        await self.db.flush()

        await create_audit_log(
            db=self.db,
            tenant_id=self.tenant.id,
            actor_user_id=self.user.id,
            target_user_id=None,
            action=AuditAction.TASK_CREATED,
        )

        return task

    async def list(self, *, project_id: int):
        result = await self.db.execute(
            select(Task).where(Task.project_id == project_id)
        )
        return result.scalars().all()

    async def get(self, *, project_id: int, task_id: int):
        result = await self.db.execute(
            select(Task).where(
                Task.project_id == project_id,
                Task.id == task_id,
            )
        )
        return result.scalar_one_or_none()

    async def delete(self, *, task: Task) -> None:
        await self.db.delete(task)

        await create_audit_log(
            db=self.db,
            tenant_id=self.tenant.id,
            actor_user_id=self.user.id,
            target_user_id=None,
            action=AuditAction.TASK_DELETED,
        )

