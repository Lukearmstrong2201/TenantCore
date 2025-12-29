from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from sqlalchemy import text


router = APIRouter()

@router.get("/health/db")
async def health_check_db(
    db: AsyncSession = Depends(get_session),
):
    await db.execute(text("SELECT 1"))
    
    return {
        "status": "ok",
        "database": "reachable",
    }
