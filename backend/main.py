
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine, get_db
from models import Base
import shutil
import os
import crud

app = FastAPI()

# Add CORS middleware to allow cross-origin requests from the web dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

UPLOAD_DIR = "images"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/api/events")
async def get_events():
    """Fetch all events from the database (public)"""
    db = SessionLocal()
    try:
        events = crud.get_events(db)
        return events
    finally:
        db.close()


@app.post("/api/events")
async def create_event(
        camera_id: str = Form(...),
        timestamp: int = Form(...),
        type: str = Form(...),
        count: int = Form(...),
        image: UploadFile = File(None)
):

    db = SessionLocal()

    image_path = None

    if image:

        path = f"{UPLOAD_DIR}/{image.filename}"

        with open(path,"wb") as buffer:
            shutil.copyfileobj(image.file,buffer)

        image_path = path

    event = {
        "camera_id":camera_id,
        "timestamp":timestamp,
        "type":type,
        "count":count,
        "image_path":image_path
    }

    crud.create_event(db,event)

    return {"status":"ok"}


@app.get("/")
async def root():
    """Root endpoint - redirect to dashboard"""
    return {"message": "EdgeVision Guard API is running"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

