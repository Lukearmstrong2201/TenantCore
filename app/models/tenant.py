from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    #Relationships
    projects = relationship(
        "Project",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )
