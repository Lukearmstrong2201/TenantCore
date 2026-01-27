from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_admin, require_tenant
from app.db.session import get_db
from app.repositories.admin.user import AdminUserRepository
from app.schemas.user import UserRead
from app.models.user import User
from app.models.tenant import Tenant


router = APIRouter(
    prefix="/admin/users",
    tags=["Admin Users"],
)


@router.get(
    "",
    response_model=list[UserRead],
    status_code=status.HTTP_200_OK,
)
async def list_users(
    _: User = Depends(require_admin),
    tenant: Tenant = Depends(require_tenant),
    db: AsyncSession = Depends(get_db),
):
    repo = AdminUserRepository(db=db, tenant=tenant)
    return await repo.list_all()


@router.get(
    "/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_id: int,
    _: User = Depends(require_admin),
    tenant: Tenant = Depends(require_tenant),
    db: AsyncSession = Depends(get_db),
):
    repo = AdminUserRepository(db=db, tenant=tenant)
    user = await repo.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user
