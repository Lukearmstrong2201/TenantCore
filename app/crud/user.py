from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password


async def get_user_by_id(
    db: AsyncSession,
    user_id: int,
) -> User | None:
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def get_user_by_email(
    db: AsyncSession,
    email: str,
) -> User | None:
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    user_in: UserCreate,
    tenant_id: int,
) -> User:
    db_user = User(
        email=user_in.email,
        is_active=user_in.is_active,
        is_admin=False,
        hashed_password=hash_password(user_in.password),
        tenant_id=tenant_id,
    )

    db.add(db_user)
    return db_user


async def get_users_by_tenant(
    db: AsyncSession,
    tenant_id: int,
) -> list[User]:
    result = await db.execute(
        select(User).where(User.tenant_id == tenant_id)
    )
    return result.scalars().all()


async def promote_user_to_admin(
    db: AsyncSession,
    *,
    user_id: int,
    tenant_id: int,
) -> User:
    result = await db.execute(
        select(User).where(
            User.id == user_id,
            User.tenant_id == tenant_id,
        )
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in tenant",
        )

    if user.is_admin:
        return user

    user.is_admin = True
    return user


async def demote_admin_user(
    db: AsyncSession,
    user_id: int,
    current_user_id: int,
    tenant_id: int,
) -> User:
    if user_id == current_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot demote yourself.",
        )

    admin_count = await count_admins_in_tenant(db, tenant_id)
    if admin_count <= 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove the last admin in the tenant.",
        )

    user = await get_user_by_id(db, user_id)
    if not user or user.tenant_id != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already not an admin.",
        )

    user.is_admin = False
    return user


async def count_admins_in_tenant(
    db: AsyncSession,
    tenant_id: int,
) -> int:
    result = await db.execute(
        select(func.count())
        .select_from(User)
        .where(
            User.tenant_id == tenant_id,
            User.is_admin == True,
        )
    )
    return result.scalar_one()


async def deactivate_user(
    db: AsyncSession,
    user_id: int,
    current_user_id: int,
    tenant_id: int,
) -> User:
    if user_id == current_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot deactivate yourself.",
        )

    user = await get_user_by_id(db, user_id)
    if not user or user.tenant_id != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already inactive.",
        )

    if user.is_admin:
        admin_count = await count_admins_in_tenant(db, tenant_id)
        if admin_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot deactivate the last admin in the tenant.",
            )

    user.is_active = False
    return user


async def reactivate_user(
    db: AsyncSession,
    user_id: int,
    tenant_id: int,
) -> User:
    user = await get_user_by_id(db, user_id)
    if not user or user.tenant_id != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    if user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already active.",
        )

    user.is_active = True
    return user
