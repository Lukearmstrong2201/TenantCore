from app.models.project_membership import ProjectRole
from app.models.user import User
from app.models.tenant import Tenant
from app.repositories.project_membership import ProjectMembershipRepository
from sqlalchemy.ext.asyncio import AsyncSession


class ProjectMembershipService:
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
        self.repo = ProjectMembershipRepository(
            db=db,
            tenant=tenant,
            actor=actor,
        )

    async def _require_owner(self, project_id: int) -> None:
        """
        Ensure the acting user is an OWNER of the project.
        """
        members = await self.repo.list_members(project_id=project_id)

        for m in members:
            if m.user_id == self.actor.id and m.role == ProjectRole.OWNER:
                return

        raise PermissionError("Only project owners can manage members")

    async def add_member(
        self,
        *,
        project_id: int,
        user_id: int,
        role: ProjectRole,
    ):
        await self._require_owner(project_id)

        return await self.repo.add_member(
            project_id=project_id,
            user_id=user_id,
            role=role,
        )

    async def update_member_role(
        self,
        *,
        project_id: int,
        user_id: int,
        role: ProjectRole,
    ) -> None:
        await self._require_owner(project_id)

        if role != ProjectRole.OWNER:
            owners = await self.repo.owner_count(project_id)
            if owners <= 1:
                raise ValueError("Cannot remove the last project owner")

        await self.repo.update_role(
            project_id=project_id,
            user_id=user_id,
            role=role,
        )

    async def remove_member(
        self,
        *,
        project_id: int,
        user_id: int,
    ) -> None:
        await self._require_owner(project_id)

        owners = await self.repo.owner_count(project_id)
        if owners <= 1:
            raise ValueError("Cannot remove the last project owner")

        await self.repo.remove_member(
            project_id=project_id,
            user_id=user_id,
        )

    async def list_members(self, *, project_id: int):
        return await self.repo.list_members(project_id=project_id)
