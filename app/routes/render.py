import os
from fastapi import APIRouter, HTTPException
from app.services.ffmpeg_render import burn_subtitles

router = APIRouter(prefix="/render", tags=["Render"])

JOBS_DIR = "jobs"

@router.post("/{job_id}")
def render_video(job_id: str):
    job_path = os.path.join(JOBS_DIR, job_id)

    video_path = os.path.join(job_path, "input.mp4")
    ass_path = os.path.join(job_path, "subtitles.ass")
    output_path = os.path.join(job_path, "output.mp4")

    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="input.mp4 not found")

    if not os.path.exists(ass_path):
        raise HTTPException(status_code=404, detail="subtitles.ass not found")

    burn_subtitles(video_path, ass_path, output_path)

    return {
        "job_id": job_id,
        "status": "video_rendered"
    }
