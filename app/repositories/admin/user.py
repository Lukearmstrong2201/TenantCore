from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User


class AdminUserRepository:
    def __init__(self, *, db: AsyncSession):
        self.db = db

    async def list_all(self) -> list[User]:
        result = await self.db.execute(
            select(User)
        )
        return result.scalars().all()

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
