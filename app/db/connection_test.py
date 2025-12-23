from sqlalchemy import text
from app.core.database import engine


async def test_db_connection():
    if engine is None:
        raise RuntimeError("Database engine not initialized")
    

    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
