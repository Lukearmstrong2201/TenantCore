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
        is_admin=user_in.is_admin,
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


