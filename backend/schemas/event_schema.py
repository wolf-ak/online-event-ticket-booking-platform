from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    event_date: datetime
    ticket_price: int
    venue_id: int
    organizer_id: int

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class EventStatusUpdate(BaseModel):
    status: str