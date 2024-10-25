from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
from services.admin_interface import AdminInterface
from models.ingestion_job import IngestionJob

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
admin_interface = AdminInterface()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class IngestionJobCreate(BaseModel):
    title: str
    author: str
    genre: str
    description: str

@app.post("/ingestion-jobs/")
async def create_ingestion_job(job: IngestionJobCreate, token: str = Depends(oauth2_scheme)):
    # TODO: Implement proper authentication
    return admin_interface.create_ingestion_job(job.dict())

@app.post("/ingestion-jobs/{job_id}/upload")
async def upload_manuscript(job_id: str, file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    # TODO: Implement proper authentication
    return await admin_interface.upload_manuscript(job_id, file)

@app.get("/ingestion-jobs/{job_id}/progress")
async def monitor_ingestion_progress(job_id: str, token: str = Depends(oauth2_scheme)):
    # TODO: Implement proper authentication
    return admin_interface.monitor_ingestion_progress(job_id)
