from redis.asyncio import ConnectionPool
from redis.asyncio.client import Redis

from src.app.schemas import JobOutSchema
from .config import get_settings

settings = get_settings()

redis_connection_pool = ConnectionPool.from_url(
    "redis://localhost:6379?decode_responses=True"
)


class RedisManager:
    def __init__(self):
        self.redis = Redis(connection_pool=redis_connection_pool)

    async def get_job(self, job_id: int, add_popularity: bool = True):
        """Retrieve a job from Redis and increase its access count."""
        job = await self.redis.hgetall(f"job:{job_id}")
        if add_popularity:
            await self.redis.zincrby("jobs:popular", 1, job_id)
        return job if job else None

    async def save_job(self, job_data: JobOutSchema):
        """Save a job in Redis if it's frequently accessed."""
        job_key = f"job:{job_data.id}"

        score = await self.redis.zscore("jobs:popular", job_data.id)
        if not score:
            await self.redis.zadd("jobs:popular", {str(job_data.id): 1})
        elif score >= 3:
            await self.redis.hset(job_key, mapping=job_data.model_dump(mode="json"))
            await self.redis.expire(job_key, 3600)

    async def get_top_jobs(self, limit: int = 10):
        """Get most frequently accessed jobs."""
        jobs_popularity = await self.redis.zrevrange("jobs:popular", 0, limit - 1, withscores=True)
        jobs = []
        for job_data in jobs_popularity:
            if job_data[1] >= 3:
                job = await self.get_job(int(job_data[0]), add_popularity=False)
                jobs.append({"id": job_data[0], **job})
        return jobs

    async def delete_job(self, job_id: int):
        """Delete a job from Redis and remove it from the popular list."""
        await self.redis.delete(f"job:{job_id}")
        await self.redis.zrem("jobs:popular", job_id)


def get_redis_db() -> RedisManager:
    return RedisManager()
