from fastapi import FastAPI


from src.core.config import get_settings
from src.core.database import get_db, DBManager

settings = get_settings()

app = FastAPI(
    **settings.fastapi_kwargs
)


@app.on_event('startup')
async def on_startup():
    from src.app.models import Job
    db = await get_db()
    await db.create_tables()
