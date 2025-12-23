from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from app.db.session import get_database_url

engine: AsyncEngine | None = None


def init_engine() -> None:
    global engine
    engine = create_async_engine(
        get_database_url(),
        echo=False,
        pool_pre_ping=True,
    )


async def close_engine() -> None:
    global engine
    if engine:
        await engine.dispose()
        engine = None
