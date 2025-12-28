from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db_session
from app.models import HealthCheck


router = APIRouter()

@router.get("/health/db")
async def health_check_db(
    db: AsyncSession = Depends(get_db_session),
):
    result = await db.execute(select(HealthCheck))
    rows = result.scalars().all()

    return {
        "status": "ok",
        "rows_in_db": len(rows),
    }
