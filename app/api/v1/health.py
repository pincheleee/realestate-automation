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
    try:
        # Check database connection
        await db.execute(text("SELECT 1"))

        # Check Redis connection
        await cache.redis.ping()
        
        return {
            "status": "healthy",
            "version": settings.VERSION,
            "database": "connected",
            "cache": "connected",
            "environment": settings.ENVIRONMENT,
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "version": settings.VERSION,
            "database": "disconnected",
            "cache": "disconnected",
            "error": str(e),
        } 