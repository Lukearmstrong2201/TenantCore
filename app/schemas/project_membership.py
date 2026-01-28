from pydantic import BaseModel
from app.models.project_membership import ProjectRole


class ProjectMemberAdd(BaseModel):
    user_id: int
    role: ProjectRole = ProjectRole.MEMBER


class ProjectMemberUpdate(BaseModel):
    role: ProjectRole
