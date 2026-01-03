from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    """
    Shared project fields.
    """
    name: str = Field(..., max_length=255)


class ProjectCreate(ProjectBase):
    """
    Schema used when creating a project.
    """
    pass


class ProjectRead(ProjectBase):
    """
    Schema returned from the API.
    """
    id: int
    tenant_id: int

    class Config:
        from_attributes = True
