from fastapi import FastAPI


from src.core.config import get_settings

settings = get_settings()

app = FastAPI(
    **settings.fastapi_kwargs
)
