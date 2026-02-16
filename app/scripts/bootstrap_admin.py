import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import hash_password
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.models.tenant import Tenant


SYSTEM_TENANT_NAME = "System"
ADMIN_EMAIL = "admin@example.com" #CHANGE AS REQUIRED
ADMIN_PASSWORD = "ChangeMe123!"  # CHANGE IMMEDIATELY


async def bootstrap() -> None:
    # Safety — NEVER allow accidental prod execution
    if not settings.allow_bootstrap:
        raise RuntimeError(
            "Bootstrap disabled. Set ALLOW_BOOTSTRAP=true to run this script."
        )

    async with AsyncSessionLocal() as db:  # type: AsyncSession
        try:
            # Get or create System tenant
            result = await db.execute(
                select(Tenant).where(Tenant.name == SYSTEM_TENANT_NAME)
            )
            tenant = result.scalar_one_or_none()

            if not tenant:
                tenant = Tenant(name=SYSTEM_TENANT_NAME)
                db.add(tenant)
                await db.flush()  # assigns tenant.id

            # Check if admin already exists
            result = await db.execute(
                select(User).where(User.email == ADMIN_EMAIL)
            )
            if result.scalar_one_or_none():
                print("Admin user already exists — bootstrap skipped")
                return

            # Create admin user
            admin = User(
                email=ADMIN_EMAIL,
                hashed_password=hash_password(ADMIN_PASSWORD),
                is_admin=True,
                is_active=True,
                tenant_id=tenant.id,
            )

            db.add(admin)
            await db.commit()

            print("\nAdmin bootstrapped successfully")
            print(f"Tenant: {SYSTEM_TENANT_NAME}")
            print(f"Email: {ADMIN_EMAIL}")
            print(f"Password: {ADMIN_PASSWORD} (CHANGE IMMEDIATELY)\n")

        except Exception:
            await db.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(bootstrap())
