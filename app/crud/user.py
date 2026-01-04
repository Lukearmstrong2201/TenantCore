from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def get_by_email(
    db: Session,
    *,
    email: str,
    tenant_id: int,
) -> User | None:
    return (
        db.query(User)
        .filter(
            User.email == email,
            User.tenant_id == tenant_id,
        )
        .first()
    )


def create(
    db: Session,
    *,
    user_in: UserCreate,
    tenant_id: int,
) -> User:
    db_user = User(
        email=user_in.email,
        is_active=user_in.is_active,
        is_admin=user_in.is_admin,
        tenant_id=tenant_id,
        hashed_password=user_in.password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
