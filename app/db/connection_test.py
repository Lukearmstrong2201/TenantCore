import asyncpg
from app.db.session import get_database_url


async def test_db_connection():
    conn = await asyncpg.connect(get_database_url())
    await conn.close()
