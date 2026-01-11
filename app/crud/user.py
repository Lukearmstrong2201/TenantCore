from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
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
        tenant_id=tenant_id
    )

    db.add(db_user)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    
    
    await db.refresh(db_user)
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
    """
    Promote a user to admin within the same tenant.
    """
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
    await db.commit()
    await db.refresh(user)

    return user


async def demote_admin_user(
    db: AsyncSession,
    user_id: int,
    tenant_id: int,
) -> User:
    """
    Demote an admin user back to a regular user within the same tenant.
    """
    result = await db.execute(
        select(User).where(
            User.id == user_id,
            User.tenant_id == tenant_id,
            User.is_admin.is_(True),
        )
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin user not found in tenant",
        )

    user.is_admin = False
    await db.commit()
    await db.refresh(user)
    return user




