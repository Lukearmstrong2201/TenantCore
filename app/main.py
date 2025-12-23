from fastapi import FastAPI
import logging
from app.api.v1 import router as v1_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.lifespan import lifespan
from app.db.connection_test import test_db_connection


setup_logging()

logger = logging.getLogger(__name__)
logger.info("Starting TenantCore API")

app = FastAPI(title=settings.app_name,lifespan=lifespan,)

app.include_router(v1_router)