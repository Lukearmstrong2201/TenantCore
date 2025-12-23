import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import init_engine, close_engine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("TenantCore startup sequence initiated")

    # Startup
    init_engine()
    logger.info("Database engine initialized")

    yield

    # Shutdown
    logger.info("TenantCore shutdown sequence initiated")
    await close_engine()
    logger.info("Database engine closed")
