from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps.auth import get_current_user
from app.api.deps.tenant import get_current_tenant

from app.models.user import User
from app.models.tenant import Tenant
from app.schemas.project_membership import ProjectMemberAdd, ProjectMemberUpdate
from app.services.project_membership_service import ProjectMembershipService

router = APIRouter(
    prefix="/projects/{project_id}/members",
    tags=["Project Members"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_member(
    project_id: int,
    payload: ProjectMemberAdd,
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant),
    current_user: User = Depends(get_current_user),
):
    service = ProjectMembershipService(
        db=db,
        tenant=tenant,
        actor=current_user,
    )

    try:
        return await service.add_member(
            project_id=project_id,
            user_id=payload.user_id,
            role=payload.role,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.patch("/{user_id}")
async def update_member(
    project_id: int,
    user_id: int,
    payload: ProjectMemberUpdate,
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant),
    current_user: User = Depends(get_current_user),
):
    service = ProjectMembershipService(
        db=db,
        tenant=tenant,
        actor=current_user,
    )

    try:
        await service.update_member_role(
            project_id=project_id,
            user_id=user_id,
            role=payload.role,
        )
        return {"status": "updated"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    project_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant),
    current_user: User = Depends(get_current_user),
):
    service = ProjectMembershipService(
        db=db,
        tenant=tenant,
        actor=current_user,
    )

    try:
        await service.remove_member(
            project_id=project_id,
            user_id=user_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("")
async def list_members(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant),
    current_user: User = Depends(get_current_user),
):
    service = ProjectMembershipService(
        db=db,
        tenant=tenant,
        actor=current_user,
    )

    return await service.list_members(project_id=project_id)
