from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, project_id: int, title: str, description: str | None):
        task = Task(
            project_id=project_id,
            title=title,
            description=description,
        )
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def list(self, project_id: int):
        result = await self.db.execute(
            select(Task).where(Task.project_id == project_id)
        )
        return result.scalars().all()

    async def get(self, project_id: int, task_id: int):
        result = await self.db.execute(
            select(Task).where(
                Task.project_id == project_id,
                Task.id == task_id,
            )
        )
        return result.scalar_one_or_none()

    async def delete(self, task: Task):
        await self.db.delete(task)
        await self.db.commit()
