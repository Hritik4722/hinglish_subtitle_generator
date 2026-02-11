import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

JOBS_DIR = "jobs"

@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    # 1. Validate file type (basic)
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Only video files are allowed")

    # 2. Generate job_id
    job_id = str(uuid.uuid4())

    # 3. Create job folder
    job_path = os.path.join(JOBS_DIR, job_id)
    os.makedirs(job_path, exist_ok=True)

    # 4. Save video as input.mp4
    video_path = os.path.join(job_path, "input.mp4")

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 5. Return job_id
    return {
        "job_id": job_id,
        "message": "Video uploaded successfully"
    }
