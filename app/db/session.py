from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.core.config import get_settings

settings = get_settings()

# Create async engine (expects postgresql+asyncpg:// URI)
engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    echo=settings.ENVIRONMENT == "development",
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Create sync engine for migrations (swap asyncpg back to psycopg2)
_sync_uri = settings.SQLALCHEMY_DATABASE_URI.replace("+asyncpg", "")
sync_engine = create_engine(
    _sync_uri,
    pool_pre_ping=True,
    echo=settings.ENVIRONMENT == "development",
)

# Create sync session factory
SessionLocal = sessionmaker(
    sync_engine,
    autocommit=False,
    autoflush=False,
)


async def get_db():
    """FastAPI dependency that yields an async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def get_sync_db():
    """Dependency that yields a sync database session (for migrations)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
