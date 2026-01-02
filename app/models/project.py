from sqlalchemy import Column, Integer, String
from app.db.base_class import Base
from app.models.mixins import TenantScopedMixin


class Project(TenantScopedMixin, Base):
    """
    A project belongs to a tenant.
    """

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
