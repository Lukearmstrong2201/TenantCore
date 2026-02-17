from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import get_current_user
from app.api.deps import require_admin
from app.crud.user import create_user
from app.crud.user import get_users_by_tenant
from app.crud.user import promote_user_to_admin
from app.crud.user import demote_admin_user
from app.crud.user import reactivate_user, deactivate_user
from app.crud.audit_log import create_audit_log

from app.models.audit_action import AuditAction
from app.models.user import User
from app.schemas.user import UserRead, UserCreate

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/whoami")
async def who_am_i(
    current_user: User = Depends(get_current_user),
):
    """
    Debug endpoint to verify resolved user + tenant context.
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "tenant_id": current_user.tenant_id,
        "is_admin": current_user.is_admin,
    }


@router.get("/me", response_model=UserRead)
async def read_current_user(
    current_user: User = Depends(get_current_user),
):
    """
    Get tennant currently logged in.
    """
    return current_user


@router.get("/", response_model=list[UserRead])
async def read_users_in_tenant(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    Get users belonging to the tenant.
    """
    return await get_users_by_tenant(
        db,
        tenant_id=current_user.tenant_id,
    )

# Temporary for testing
@router.post("/", response_model=UserRead)
async def create_user_endpoint(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return await create_user(db, user_in,tenant_id=current_user.tenant_id,)


@router.post("/{user_id}/promote", response_model=UserRead)
async def promote_user(
    user_id: int,
    current_admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    Promote a user to admin within the same tenant.
    """
    if current_admin.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot promote yourself",
        )

    promoted_user = await promote_user_to_admin(
        db,
        user_id=user_id,
        tenant_id=current_admin.tenant_id,
    )

    await create_audit_log(
    db=db,
    tenant_id=current_admin.tenant_id,
    actor_user_id=current_admin.id,
    target_user_id=promoted_user.id,
    action=AuditAction.PROMOTE_ADMIN,
)

    return promoted_user


@router.patch("/{user_id}/demote", response_model=UserRead)
async def demote_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """
    Demote an admin user to a regular user in the same tenant.
    Can only be performed by an admin.
    """
    # Block self-demotion
    if current_admin.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot demote yourself.",
        )
    
    # Call the demote_admin_user function with all required arguments
    demoted_user = await demote_admin_user(
        db=db, 
        user_id=user_id,
        current_user_id=current_admin.id,
        tenant_id=current_admin.tenant_id
    )
    
    await create_audit_log(
        db=db,
        tenant_id=current_admin.tenant_id,
        actor_user_id=current_admin.id,
        target_user_id=demoted_user.id,
        action=AuditAction.DEMOTE_ADMIN,
)
    return demoted_user


@router.patch("/{user_id}/deactivate", response_model=UserRead)
async def deactivate_user_endpoint(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """
    Deactivate a user in the same tenant.
    """
    return await deactivate_user(
        db=db,
        user_id=user_id,
        current_user_id=current_admin.id,
        tenant_id=current_admin.tenant_id,
    )


@router.patch("/{user_id}/reactivate", response_model=UserRead)
async def reactivate_user_endpoint(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """
    Reactivate a user in the same tenant.
    """
    return await reactivate_user(
        db=db,
        user_id=user_id,
        tenant_id=current_admin.tenant_id,
    )

