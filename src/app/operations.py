from fastapi.exceptions import HTTPException
import sqlalchemy as sa
from src.core.database import DBManager
from .models import Job


async def get_job_by_title_company(db_session: DBManager, job_title: str, job_company: str) -> Job | None:
    query = sa.select(Job).where(
        Job.title == job_title.strip(), Job.company == job_company.strip())
    async with db_session.begin() as session:
        job = await session.scalar(query)

    return job


async def create_job(db_session: DBManager, *, job_title: str, job_description: str, job_company: str) -> Job:
    if await get_job_by_title_company(db_session, job_title=job_title, job_company=job_company):
        raise HTTPException(400, "Job is already exist for this company")
    new_job = Job(title=job_title.strip(), description=job_description.strip(),
                  company=job_company.strip())
    async with db_session.begin() as session:
        session.add(new_job)

    return new_job


async def get_all_jobs(db_session: DBManager):
    query = sa.select(Job)
    async with db_session.begin() as session:
        jobs = await session.scalars(query)

    return jobs


async def get_job_by_id(db_session: DBManager,*, job_id: int) -> Job:
    query = sa.select(Job).where(Job.id == job_id)
    async with db_session.begin() as session:
        job = await session.scalar(query)
    if not job:
        raise HTTPException(404, "There is no job with this id")
    return job


async def search_job_by_title(db_session: DBManager, *, search_data: str):
    query = sa.select(Job).where(Job.title.like(f"%{search_data}%"))
    async with db_session.begin() as session:
        jobs = await session.scalars(query)

    return jobs


async def update_job(db_session: DBManager, job_id, *, job_title: str, job_description: str, job_company: str) -> Job:
    job = await get_job_by_id(db_session, job_id=job_id)
    job.title = job_title.strip()
    job.description = job_description.strip()
    job.company = job_company.strip()
    async with db_session.begin() as session:
        session.add(job)
    return await get_job_by_id(db_session, job_id=job_id)


async def del_job(db_session: DBManager, job_id) -> None:
    job = await get_job_by_id(db_session, job_id=job_id)
    async with db_session.begin() as session:
        await session.delete(job)
