from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.project_membership import ProjectMembership, ProjectRole
from app.models.user import User
from app.models.tenant import Tenant


class ProjectMembershipRepository:
    def __init__(
        self,
        *,
        db: AsyncSession,
        tenant: Tenant,
        actor: User,
    ):
        self.db = db
        self.tenant = tenant
        self.actor = actor

    async def add_member(
        self,
        *,
        project_id: int,
        user_id: int,
        role: ProjectRole,
    ) -> ProjectMembership:
        membership = ProjectMembership(
            tenant_id=self.tenant.id,
            project_id=project_id,
            user_id=user_id,
            role=role,
        )

        self.db.add(membership)
        await self.db.commit()
        await self.db.refresh(membership)

        return membership

    async def update_role(
        self,
        *,
        project_id: int,
        user_id: int,
        role: ProjectRole,
    ) -> None:
        stmt = (
            select(ProjectMembership)
            .where(
                ProjectMembership.project_id == project_id,
                ProjectMembership.user_id == user_id,
                ProjectMembership.tenant_id == self.tenant.id,
            )
        )

        membership = (await self.db.execute(stmt)).scalar_one()

        membership.role = role
        await self.db.commit()

    async def remove_member(
        self,
        *,
        project_id: int,
        user_id: int,
    ) -> None:
        stmt = (
            select(ProjectMembership)
            .where(
                ProjectMembership.project_id == project_id,
                ProjectMembership.user_id == user_id,
                ProjectMembership.tenant_id == self.tenant.id,
            )
        )

        membership = (await self.db.execute(stmt)).scalar_one()
        await self.db.delete(membership)
        await self.db.commit()

    async def owner_count(self, project_id: int) -> int:
        stmt = (
            select(func.count())
            .select_from(ProjectMembership)
            .where(
                ProjectMembership.project_id == project_id,
                ProjectMembership.tenant_id == self.tenant.id,
                ProjectMembership.role == ProjectRole.OWNER,
            )
        )

        return (await self.db.execute(stmt)).scalar_one()
