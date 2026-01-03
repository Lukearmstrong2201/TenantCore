from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import declared_attr


class TenantScopedMixin:
    __abstract__ = True
    """
    Mixin that adds tenant ownership to a model.
    """

    @declared_attr
    def tenant_id(cls):
        return Column(
            Integer,
            ForeignKey("tenants.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    
            
        
