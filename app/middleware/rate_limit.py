from fastapi import Request, HTTPException
from redis import asyncio as aioredis
from app.core.config import get_settings
from app.core.exceptions import ForbiddenException
import time
from typing import Optional

settings = get_settings()

class RateLimiter:
    def __init__(self):
        self.redis = aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            encoding="utf8",
            decode_responses=True,
        )

    async def is_rate_limited(
        self, key: str, limit: int, window: int
    ) -> tuple[bool, Optional[int]]:
        current = await self.redis.get(key)
        if current is None:
            await self.redis.setex(key, window, 1)
            return False, limit - 1

        current = int(current)
        if current >= limit:
            return True, 0

        await self.redis.incr(key)
        return False, limit - current - 1

    async def get_remaining_requests(
        self, key: str, limit: int, window: int
    ) -> int:
        current = await self.redis.get(key)
        if current is None:
            return limit
        return max(0, limit - int(current))

rate_limiter = RateLimiter()

async def rate_limit_middleware(request: Request, call_next):
    limit = 100
    window = 60
    key_prefix = "rate_limit"

    client_ip = request.client.host
    key = f"{key_prefix}:{client_ip}"

    is_limited, remaining = await rate_limiter.is_rate_limited(key, limit, window)

    if is_limited:
        raise ForbiddenException("Rate limit exceeded")

    response = await call_next(request)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Limit"] = str(limit)
    response.headers["X-RateLimit-Reset"] = str(int(time.time()) + window)

    return response 