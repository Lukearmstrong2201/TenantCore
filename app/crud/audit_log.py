from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.audit_log import AuditLog


async def create_audit_log(
    db: AsyncSession,
    *,
    tenant_id: int,
    actor_user_id: int,
    action,
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


async def list_audit_logs(
    *,
    db: AsyncSession,
    tenant_id: int,
    limit: int = 50,
    offset: int = 0,
):
    stmt = (
        select(AuditLog)
        .where(AuditLog.tenant_id == tenant_id)
        .options(
            selectinload(AuditLog.actor_user),
            selectinload(AuditLog.target_user),
        )
        .order_by(AuditLog.created_at.desc())
        .limit(limit)
        .offset(offset)
    )

    result = await db.execute(stmt)
    return result.scalars().all()
