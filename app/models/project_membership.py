from sqlalchemy import Column, Integer, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.mixins import TenantScopedMixin


class ProjectMembership(TenantScopedMixin, Base):
    __tablename__ = "project_memberships"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )

    role = Column(
        Enum(
            "OWNER",
            "ADMIN",
            "MEMBER",
            "VIEWER",
            name="project_role",
        ),
        nullable=False,
        default="MEMBER",
    )

    __table_args__ = (
        UniqueConstraint("user_id", "project_id", name="uq_user_project"),
    )

    
    user = relationship("User")
    project = relationship("Project")
