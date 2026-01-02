from pydantic import BaseModel, Field


class TenantBase(BaseModel):
    """
    Shared tenant fields.
    """
    name: str = Field(..., max_length=255)


class TenantCreate(TenantBase):
    """
    Schema used when creating a tenant
    """
    pass


class TenantRead(TenantBase):
    """
    Schema used when returning a tenant from the API
    """
    id: int

    class Config:
        from_attributes = True  # Pydantic (ORM)
