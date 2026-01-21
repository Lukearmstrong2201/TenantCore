from app.api.deps.auth import (
    get_current_user,
    require_admin,
)

from app.api.deps.tenant import (
    get_current_tenant,
    require_tenant,
)

__all__ = [
    "get_current_user",
    "require_admin",
    "get_current_tenant",
    "require_tenant",
]
