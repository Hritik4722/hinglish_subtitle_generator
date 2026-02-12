import os
import json
from fastapi import APIRouter, HTTPException

from app.services.segment import segment_creator_mode

router = APIRouter(prefix="/segment", tags=["Segmentation"])

JOBS_DIR = "jobs"


@router.post("/{job_id}")
def segment_job(job_id: str):
    job_path = os.path.join(JOBS_DIR, job_id)
    hinglish_path = os.path.join(job_path, "hinglish.json")
    segmented_path = os.path.join(job_path, "segmented.json")

    if not os.path.exists(hinglish_path):
        raise HTTPException(status_code=404, detail="hinglish.json not found")

    with open(hinglish_path, "r", encoding="utf-8") as f:
        segments = json.load(f)

    segmented = segment_creator_mode(segments)

    with open(segmented_path, "w", encoding="utf-8") as f:
        json.dump(segmented, f, ensure_ascii=False, indent=2)

    return {
        "job_id": job_id,
        "status": "segmentation_completed"
    }
