from app.db.base_class import Base

# Import all models so Alembic can see them
from app.models.health_check import HealthCheck
from app.models.tenant import Tenant
from app.models.project import Project