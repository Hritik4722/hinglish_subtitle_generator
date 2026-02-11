import os
import json
from fastapi import APIRouter,HTTPException
from app.services.hinglish import convert_hinglish

router = APIRouter(prefix="/cleanup", tags=["Cleanup"])

JOBS_DIR = "jobs"

@router.post("/{job_id}")
def cleanup(job_id: str):
    job_path = os.path.join(JOBS_DIR, job_id)
    raw_path = os.path.join(job_path, "raw.json")
    hinglish_path = os.path.join(job_path, "hinglish.json")

    if not os.path.exists(job_path):
        raise HTTPException(status_code=404, detail="Job not found")
    
    with open(raw_path, "r",encoding="utf-8") as f:
        segments = json.load(f)
    
    cleaned_segments = convert_hinglish(segments)

    with open(hinglish_path,"w", encoding="utf-8") as f:
        json.dump(cleaned_segments,f,ensure_ascii=False, indent=2)

    return {
        "job_id": job_id,
        "status": "hinglish_generated"
    }
