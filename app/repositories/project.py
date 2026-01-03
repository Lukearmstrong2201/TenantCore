from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.tenant import Tenant


def create_project_for_tenant(
    *,
    db: Session,
    tenant: Tenant,
    name: str,
) -> Project:
    """
    Create a project scoped to a tenant.
    """
    project = Project(
        name=name,
        tenant_id=tenant.id,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project
