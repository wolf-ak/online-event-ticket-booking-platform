from sqlalchemy.orm import Session
from backend.models.venue import Venue
from backend.models.event import Event
from backend.models.seat import Seat
from backend.models.order import Order

def create_venue(venue_data, db: Session):
    new_venue = Venue(**venue_data.model_dump())
    db.add(new_venue)
    db.commit()
    db.refresh(new_venue)
    return new_venue

def create_event(event_data, db: Session):
    new_event = Event(**event_data.model_dump())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

def update_event_status(event_id: int, status_data, db: Session):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        return False
    event.status = status_data.status
    db.commit()
    return True

def create_seats(event_id: int, seats_data: list, db: Session):
    seats = [Seat(event_id=event_id, **seat.model_dump()) for seat in seats_data]
    db.bulk_save_objects(seats)
    db.commit()
    return {"message": f"{len(seats)} seats created successfully."}

def get_event_by_id(event_id: int, db: Session):
    return db.query(Event).filter(Event.id == event_id).first()

def get_event_orders(event_id: int, db: Session):
    return db.query(Order).filter(Order.event_id == event_id).all()