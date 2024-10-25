from pydantic import BaseModel
from uuid import uuid4

class IngestionJob(BaseModel):
    id: str = str(uuid4())
    title: str
    author: str
    genre: str
    description: str
    status: str = "pending"
