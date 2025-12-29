import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import init_engine, close_engine, create_tables

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("TenantCore startup sequence initiated")

    # Startup
    init_engine()
    logger.info("Database engine initialized")

    await create_tables()
    """
    TEMPORARY
    Will be replaced by Alembic migrations.
    """
    logger.info("Database tables created")

    yield

    # Shutdown
    logger.info("TenantCore shutdown sequence initiated")
    await close_engine()
    logger.info("Database engine closed")
