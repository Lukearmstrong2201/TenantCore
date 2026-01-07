from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

# Create the async database engine
# This manages the connection pool to PostgreSQL
# `echo` prints SQL queries to the console in debug mode
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
)

# Create a session factory
# Each request gets its own AsyncSession
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

# FastAPI dependency for database access
# Opens a session at the start of a request
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
