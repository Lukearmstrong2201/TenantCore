from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog

async def create_audit_log(
    db: AsyncSession,
    *,
    tenant_id: int,
    actor_user_id: int,
    action: str,
    target_user_id: int | None = None,
    detail: str | None = None,
) -> None:
    log = AuditLog(
        tenant_id=tenant_id,
        actor_user_id=actor_user_id,
        target_user_id=target_user_id,
        action=action,
        detail=detail,
    )

    db.add(log)
    await db.commit()
