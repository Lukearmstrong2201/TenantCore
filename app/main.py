from fastapi import FastAPI
from app.api.health import router as health_router
from app.core.config import settings
from app.core.logging import setup_logging

import logging


setup_logging()

logger = logging.getLogger(__name__)

logger.info("Starting TenantCore API")

app = FastAPI(title=settings.app_name)

app.include_router(health_router)