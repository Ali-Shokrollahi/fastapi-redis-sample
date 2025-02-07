from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class JobInSchema(BaseModel):
    title: str = Field(min_length=3, max_length=128)
    description: str
    company: str = Field(min_length=3, max_length=128)


class JobOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    company: str
    created_at: datetime
    updated_at: str
