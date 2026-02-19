from datetime import datetime
from pydantic import BaseModel

from app.models.audit_action import AuditAction


class AuditUserInfo(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class AuditLogRead(BaseModel):
    id: int
    action: AuditAction
    target_user_id: int | None
    action: AuditAction
    detail: str | None
    created_at: datetime

    class Config:
        from_attributes = True
