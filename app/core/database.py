from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from app.core.config import settings
from sqlalchemy import text
from app.db.base import Base


engine: AsyncEngine | None = None


def init_engine() -> None:
    global engine
    engine = create_async_engine(
        settings.database_url,
        echo=False,
        pool_pre_ping=True,
    )


async def close_engine() -> None:
    global engine
    if engine:
        await engine.dispose()
        engine = None


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)