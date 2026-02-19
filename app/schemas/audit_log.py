from datetime import datetime
from pydantic import BaseModel

from app.models.audit_action import AuditAction


class AuditLogRead(BaseModel):
    id: int
    actor_user_id: int
    target_user_id: int | None
    action: AuditAction
    detail: str | None
    created_at: datetime

    class Config:
        from_attributes = True
