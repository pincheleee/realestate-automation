from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.cache import cache
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Health check endpoint that verifies database and cache connections."""
    db_status = "connected"
    cache_status = "connected"
    errors = []

    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = "disconnected"
        errors.append(f"database: {e}")

    try:
        await cache.redis.ping()
    except Exception as e:
        cache_status = "disconnected"
        errors.append(f"cache: {e}")

    is_healthy = db_status == "connected" and cache_status == "connected"

    response = {
        "status": "healthy" if is_healthy else "unhealthy",
        "version": settings.VERSION,
        "database": db_status,
        "cache": cache_status,
        "environment": settings.ENVIRONMENT,
    }
    if errors:
        response["errors"] = errors
    return response
