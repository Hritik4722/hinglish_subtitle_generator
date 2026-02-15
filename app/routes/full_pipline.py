from fastapi import APIRouter
from app.services.pipeline import full_pipeline

router = APIRouter(tags=["Full pipeline"])

@router.post("/run/{job_id}")
def run_pipeline(job_id: str):
    output = full_pipeline(job_id)
    return {"status": "completed", "output": output}
