import os
import json
from fastapi import APIRouter, HTTPException
from app.services.ass_generator import generate_ass
from app.services.video_info import get_video_resolution

router = APIRouter(prefix="/ass", tags=["ASS"])

JOBS_DIR = "jobs"


@router.post("/{job_id}")
def generate_ass_file(job_id: str):
    job_path = os.path.join(JOBS_DIR, job_id)

    segmented_path = os.path.join(job_path, "segmented.json")
    ass_path = os.path.join(job_path, "subtitles.ass")
    video_path = os.path.join(job_path, "input.mp4")

    if not os.path.exists(segmented_path):
        raise HTTPException(status_code=404, detail="segmented.json not found")

    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="input.mp4 not found")

    with open(segmented_path, "r", encoding="utf-8") as f:
        subtitles = json.load(f)

    width, height = get_video_resolution(video_path)

    style_name = "reels"

    style_path = os.path.join("app", "styles", f"{style_name}.json")

    with open(style_path, "r", encoding="utf-8") as f:
        style_config = json.load(f)

    generate_ass(subtitles, ass_path, width, height, style_config)


    return {
        "job_id": job_id,
        "status": "ass_generated",
        "resolution": {
            "width": width,
            "height": height
        }
    }
