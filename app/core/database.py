from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from app.core.config import settings

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
