from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import TenantScopedMixin


class User(TenantScopedMixin, Base):
    """
    A user belongs to a tenant.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships

    audit_logs_as_actor = relationship(
        "AuditLog",
        foreign_keys="AuditLog.actor_user_id",
        back_populates="actor_user",
        cascade="all, delete-orphan",
    )

    audit_logs_as_target = relationship(
        "AuditLog",
        foreign_keys="AuditLog.target_user_id",
        back_populates="target_user",
        cascade="all, delete-orphan",
    )
