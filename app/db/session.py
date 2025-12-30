from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# Create a synchronous SQLAlchemy engine
engine = create_engine(
    settings.database_url.replace("+asyncpg", ""),
    pool_pre_ping=True,
)

# Creates DB sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Session:
    """
    FastAPI dependency that provides a database session.

    - Opens a new DB session per request
    - Ensures the session is closed after the request
    - Rolls back automatically on unhandled exceptions
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
