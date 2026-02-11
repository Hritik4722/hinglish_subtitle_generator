from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.routes.process import router as process_router
from app.routes.cleanup import router as hinglish_router

app = FastAPI(title="Subtitle Generator")

app.include_router(upload_router)
app.include_router(process_router)
app.include_router(hinglish_router)

@app.get("/")
def root():
    return {"status": "ok"}
