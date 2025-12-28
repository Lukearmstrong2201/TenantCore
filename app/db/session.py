from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
import  app.core.database as database


async def get_db_session()-> AsyncGenerator[AsyncSession, None]:
    if database.engine is None:
        raise RuntimeError("Database engine not initialized")

    AsyncSessionLocal = sessionmaker(
        bind=database.engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with AsyncSessionLocal() as session:
        yield session
