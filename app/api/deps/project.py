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
    *,
    allowed_roles: set[ProjectRole],
):
    async def _dependency(
        project_id: int,
        db: AsyncSession = Depends(get_db),
        tenant: Tenant = Depends(require_tenant),
        user: User = Depends(get_current_user),
    ) -> Project:
        stmt = (
            select(Project, ProjectMembership.role)
            .join(ProjectMembership)
            .where(
                Project.id == project_id,
                Project.tenant_id == tenant.id,
                ProjectMembership.user_id == user.id,
                ProjectMembership.tenant_id == tenant.id
            )
        )

        result = await db.execute(stmt)
        row = result.first()

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found or no access",
            )

        project, role = row

        if role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient project permissions",
            )

        return project

    return _dependency

