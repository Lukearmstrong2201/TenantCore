from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings
from app.db.base import Base
from typing import AsyncGenerator


engine: AsyncEngine | None = None
SessionLocal: async_sessionmaker[AsyncSession] | None = None


def init_engine() -> None:
    global engine, SessionLocal

    engine = create_async_engine(
        settings.database_url,
        echo=False,
        pool_pre_ping=True,
    )

    SessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def close_engine() -> None:
    global engine, SessionLocal

    if engine:
        await engine.dispose()

        engine = None
        SessionLocal = None


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if SessionLocal is None:
        raise RuntimeError("SessionLocal not initialized")

    async with SessionLocal() as session:
        yield session


async def create_tables() -> None:
    """
    Temporary helper.
    Will be removed once Alembic is introduced.
    """
    if engine is None:
        raise RuntimeError("Engine not initialised")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)