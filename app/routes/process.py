import os
from fastapi import APIRouter, HTTPException

from app.services.audio import extract_audio
from app.services.whisper_stt import transcribe_audio
from app.services.sarvam_stt import sarvam_stt

router = APIRouter()

JOBS_DIR = "jobs"

@router.post("/process/{job_id}")
def process_job(job_id:str):
    job_path = os.path.join(JOBS_DIR,job_id)

    if not os.path.exists(job_path):
        raise HTTPException(status_code=404,detail="job not found")
    
    video_path = os.path.join(job_path, "input.mp4")
    audio_path = os.path.join(job_path, "audio.wav")
    transcript_path = os.path.join(job_path, "raw.json")

    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="input vidoe is missing")
    
    extract_audio(video_path, audio_path)

    # transcribe_audio(audio_path,transcript_path,"Hi")
    sarvam_stt(audio_path,transcript_path,"hi-IN")

    return {
        "job_id": job_id,
        "status": "transcription_completed"
    }