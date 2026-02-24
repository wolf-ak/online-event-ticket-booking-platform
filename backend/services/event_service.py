from typing import List, Optional

from sqlalchemy.orm import Session

from backend.models.venue import Venue
from backend.models.event import Event
from backend.models.seat import Seat
from backend.models.order import Order
from backend.schemas.venue_schema import VenueCreate
from backend.schemas.event_schema import EventCreate, EventStatusUpdate
from backend.schemas.seat_schema import SeatCreate


def create_venue(data: VenueCreate, db: Session):
    venue = Venue(
        name=data.name,
        city=data.city,
        total_capacity=data.total_capacity,
        address=data.address
    )

    db.add(venue)
    db.commit()
    db.refresh(venue)
    return venue


def create_event(data: EventCreate, db: Session):
    event = Event(
        name=data.name,
        description=data.description,
        category=data.category,
        event_date=data.event_date,
        ticket_price=data.ticket_price,
        venue_id=data.venue_id,
        organizer_id=data.organizer_id
    )

    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def update_event_status(event_id: int, data: EventStatusUpdate, db: Session) -> bool:
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        return False

    event.status = data.status
    db.commit()
    return True


def create_seats(event_id: int, seats: List[SeatCreate], db: Session):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        return None

    created = []
    for seat_data in seats:
        seat = Seat(
            event_id=event_id,
            seat_number=seat_data.seat_number,
            status=seat_data.status
        )
        db.add(seat)
        created.append(seat)

    db.commit()
    return created


def get_event_by_id(event_id: int, db: Session) -> Optional[Event]:
    return db.query(Event).filter(Event.id == event_id).first()


def get_event_orders(event_id: int, db: Session):
    return db.query(Order).filter(Order.event_id == event_id).all()
