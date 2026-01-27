from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.project import Project
from app.models.project_membership import ProjectMembership, ProjectRole
from app.models.user import User
from app.api.deps import get_current_user, require_tenant
from app.models.tenant import Tenant

def require_project_access(
    allowed_roles: set[ProjectRole] | None = None,
):
    async def dependency(
        project_id: int,
        db: AsyncSession = Depends(get_db),
        tenant: Tenant = Depends(require_tenant),
        user: User = Depends(get_current_user),
    ) -> Project:
        stmt = (
            select(Project)
            .join(ProjectMembership)
            .where(
                Project.id == project_id,
                Project.tenant_id == tenant.id,
                ProjectMembership.user_id == user.id,
                ProjectMembership.tenant_id == tenant.id,
            )
        )

        result = await db.execute(stmt)
        project = result.scalar_one_or_none()

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        if allowed_roles:
            role_stmt = (
                select(ProjectMembership.role)
                .where(
                    ProjectMembership.project_id == project_id,
                    ProjectMembership.user_id == user.id,
                    ProjectMembership.tenant_id == tenant.id,
                )
            )
            role = (await db.execute(role_stmt)).scalar_one()

            if role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient project permissions",
                )

        return project

    return dependency
