from models import Event
from sqlalchemy import func


def create_event(db, event):
    """Create a new event in the database"""
    db_event = Event(**event)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_events(db):
    """Fetch all events from the database, ordered by timestamp descending"""
    return db.query(Event).order_by(Event.timestamp.desc()).all()


def get_event_by_id(db, event_id: int):
    """Fetch a single event by ID"""
    return db.query(Event).filter(Event.id == event_id).first()


def get_event_stats(db):
    """Get event statistics: total count, unique cameras, unique types"""
    total_events = db.query(func.count(Event.id)).scalar()
    unique_cameras = db.query(func.count(func.distinct(Event.camera_id))).scalar()
    unique_types = db.query(func.count(func.distinct(Event.type))).scalar()
    
    # Get events per camera
    events_per_camera = db.query(
        Event.camera_id, 
        func.count(Event.id).label('count')
    ).group_by(Event.camera_id).all()
    
    # Get events per type
    events_per_type = db.query(
        Event.type, 
        func.count(Event.id).label('count')
    ).group_by(Event.type).all()
    
    return {
        "total_events": total_events,
        "unique_cameras": unique_cameras,
        "unique_types": unique_types,
        "events_per_camera": {row.camera_id: row.count for row in events_per_camera},
        "events_per_type": {row.type: row.count for row in events_per_type}
    }


def get_events_by_camera(db, camera_id: str):
    """Fetch events filtered by camera ID, ordered by timestamp descending"""
    return db.query(Event).filter(
        Event.camera_id == camera_id
    ).order_by(Event.timestamp.desc()).all()


def get_events_by_type(db, event_type: str):
    """Fetch events filtered by event type, ordered by timestamp descending"""
    return db.query(Event).filter(
        Event.type == event_type
    ).order_by(Event.timestamp.desc()).all()

