
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine, get_db
from models import Base
import shutil
import os
from typing import Optional, List
from datetime import datetime

# Import auth router
from auth import router as auth_router
import crud
from schemas import EventCreate, EventResponse

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

# Include auth router
app.include_router(auth_router)

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


@app.post("/api/events", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
        camera_id: str = Form(...),
        timestamp: int = Form(...),
        event_type: str = Form(...),
        count: int = Form(...),
        image: UploadFile = File(None)
):
    """Create a new event with proper schema validation"""
    db = SessionLocal()

    image_path = None

    if image:
        path = f"{UPLOAD_DIR}/{image.filename}"

        with open(path,"wb") as buffer:
            shutil.copyfileobj(image.file,buffer)

        image_path = path

    event_data = {
        "camera_id": camera_id,
        "timestamp": timestamp,
        "type": event_type,
        "count": count,
        "image_path": image_path
    }

    # Create event using schema validation
    event = crud.create_event(db, event_data)
    
    return event


@app.get("/api/events/{event_id}", response_model=EventResponse)
async def get_event(event_id: int):
    """Get a single event by ID"""
    db = SessionLocal()
    try:
        event = crud.get_event_by_id(db, event_id)
        if event is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Event with id {event_id} not found"
            )
        return event
    finally:
        db.close()


@app.get("/api/events/stats/summary")
async def get_event_stats():
    """Get event statistics"""
    db = SessionLocal()
    try:
        stats = crud.get_event_stats(db)
        return stats
    finally:
        db.close()


@app.get("/api/events/filter/camera/{camera_id}")
async def get_events_by_camera(camera_id: str):
    """Get events filtered by camera ID"""
    db = SessionLocal()
    try:
        events = crud.get_events_by_camera(db, camera_id)
        return events
    finally:
        db.close()


@app.get("/api/events/filter/type/{event_type}")
async def get_events_by_type(event_type: str):
    """Get events filtered by event type"""
    db = SessionLocal()
    try:
        events = crud.get_events_by_type(db, event_type)
        return events
    finally:
        db.close()


@app.get("/")
async def root():
    """Root endpoint - redirect to dashboard"""
    return {"message": "EdgeVision Guard API is running"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

