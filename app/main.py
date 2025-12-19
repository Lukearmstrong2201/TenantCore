from fastapi import FastAPI
import logging
from app.api.v1 import router as v1_router
from app.api.health import router as health_router
from app.core.config import settings
from app.core.logging import setup_logging


setup_logging()

logger = logging.getLogger(__name__)
logger.info("Starting TenantCore API")

app = FastAPI(title=settings.app_name)

app.include_router(v1_router)