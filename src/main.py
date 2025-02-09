from typing import Annotated
from fastapi import FastAPI, status, Path


from src.core.config import get_settings
from src.core.database import get_db
from src.core.dependencies import SessionDep

from src.app.schemas import JobInSchema, JobOutSchema
from src.app.operations import create_job, get_all_jobs, get_job_by_id, update_job, del_job, search_job_by_title


settings = get_settings()

app = FastAPI(
    **settings.fastapi_kwargs
)


@app.on_event('startup')
async def on_startup():
    from src.app.models import Job
    db = await get_db()
    await db.create_tables()


@app.post("/jobs", status_code=status.HTTP_201_CREATED)
async def post_job(job_data: JobInSchema, db_session: SessionDep) -> JobOutSchema:
    job = await create_job(db_session, job_title=job_data.title,
                           job_description=job_data.description, job_company=job_data.company)

    return JobOutSchema.model_validate(job)


@app.get("/jobs", status_code=status.HTTP_200_OK)
async def get_jobs(db_session: SessionDep, search: str | None = None) -> list[JobOutSchema]:
    if search:
        jobs = await search_job_by_title(db_session, search_data=search)
    else:
        jobs = await get_all_jobs(db_session)
    return [JobOutSchema.model_validate(job) for job in jobs]


@app.get("/jobs/{job_id}", status_code=status.HTTP_200_OK)
async def get_job(job_id: Annotated[int, Path(title="The ID of the job to get")], db_session: SessionDep) -> JobOutSchema:
    job = await get_job_by_id(db_session, job_id=job_id)
    return JobOutSchema.model_validate(job)


@app.put("/jobs/{job_id}", status_code=status.HTTP_200_OK)
async def put_job(job_id: Annotated[int, Path(title="The ID of the job to update")], job_data: JobInSchema, db_session: SessionDep) -> JobOutSchema:
    job = await update_job(db_session, job_id, job_title=job_data.title,
                           job_description=job_data.description, job_company=job_data.company)
    return JobOutSchema.model_validate(job)


@app.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(job_id: Annotated[int, Path(title="The ID of the job to delete")], db_session: SessionDep):
    await del_job(db_session, job_id=job_id)
    return {"Job deleted successfuly"}
