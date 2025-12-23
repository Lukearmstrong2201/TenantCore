from app.core.config import settings


def get_database_url() -> str:
    return (
        f"postgresql+asyncpg://"
        f"{settings.db_user}:{settings.db_password}"
        f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    )
