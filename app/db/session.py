from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from typing import AsyncGenerator

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db_session()-> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
