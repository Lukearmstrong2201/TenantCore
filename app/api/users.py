from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import get_current_user
from app.api.deps import require_admin
from app.crud.user import create_user
from app.crud.user import get_users_by_tenant
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

