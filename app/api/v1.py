from fastapi import APIRouter
from app.api.health import router as health_router
from app.api.users import router as users_router
from app.api.tenants import router as tenant_router
from app.api.project import router as project_router
from app.api.auth import router as auth_router
from app.api.admin_tenants import router as admin_tenants_router
from app.api.admin.users import router as admin_users_router
from app.api.admin.tenants import router as admin_tenant_router
from app.api.admin.tenant_create import router as admin_tenant_create_router



router = APIRouter(prefix="/api/v1")

router.include_router(health_router)
router.include_router(users_router)
router.include_router(tenant_router)
router.include_router(project_router)
router.include_router(auth_router)
router.include_router(admin_tenants_router)
router.include_router(admin_users_router)
router.include_router(admin_tenant_router)
router.include_router(admin_tenant_create_router)



