from models import Event


def create_event(db, event):
    db_event = Event(**event)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_events(db):
    """Fetch all events from the database, ordered by timestamp descending"""
    return db.query(Event).order_by(Event.timestamp.desc()).all()

