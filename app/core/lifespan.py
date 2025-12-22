import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("TenantCore startup sequence initiated")
    yield
    logger.info("TenantCore shutdown sequence initiated")
