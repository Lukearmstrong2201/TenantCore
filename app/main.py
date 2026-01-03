from fastapi import FastAPI
import logging
from app.api.v1 import router as v1_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.lifespan import lifespan
from app.api.project import router as project_router
from app.api.tenants import router as tenant_router


setup_logging()

logger = logging.getLogger(__name__)
logger.info("Starting TenantCore API")

app = FastAPI(title=settings.app_name,lifespan=lifespan,)

app.include_router(v1_router)
app.include_router(tenant_router)
app.include_router(project_router)

