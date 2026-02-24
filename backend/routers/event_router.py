from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.dependencies.get_db import get_db
from backend.dependencies.get_current_user import get_current_user
from backend.dependencies.roles import require_roles

from backend.schemas.venue_schema import VenueCreate, VenueResponse
from backend.schemas.event_schema import (
    EventCreate,
    EventResponse,
    EventStatusUpdate
)
from backend.schemas.seat_schema import SeatCreate

from backend.services.event_service import (
    create_venue,
    create_event,
    update_event_status,
    create_seats,
    get_event_by_id,
    get_event_orders
)

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


# -----------------------------------
# Create Venue (Admin)
# -----------------------------------
@router.post("/venues", response_model=VenueResponse)
def add_venue(
    venue: VenueCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("admin"))
):
    return create_venue(venue, db)


# -----------------------------------
# Create Event (Admin)
# -----------------------------------
@router.post("/", response_model=EventResponse)
def add_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("admin"))
):
    return create_event(event, db)


# -----------------------------------
# Update Event Status
# -----------------------------------
@router.patch("/{event_id}/status")
def change_status(
    event_id: int,
    data: EventStatusUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("admin"))
):
    updated = update_event_status(event_id, data, db)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    return {"message": "Event status updated successfully"}


# -----------------------------------
# Add Seats to Event (Organizer)
# -----------------------------------
@router.post("/{event_id}/seats")
def add_seats(
    event_id: int,
    seats: List[SeatCreate],
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("organizer"))
):
    return create_seats(event_id, seats, db)


# -----------------------------------
# Get Single Event Details
# -----------------------------------
@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    event = get_event_by_id(event_id, db)

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    return event


# -----------------------------------
# Get Orders for an Event (Organizer)
# -----------------------------------
@router.get("/{event_id}/orders")
def view_orders(
    event_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("organizer"))
):
    return get_event_orders(event_id, db)
