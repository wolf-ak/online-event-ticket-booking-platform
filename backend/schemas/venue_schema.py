from pydantic import BaseModel
from datetime import datetime


class VenueBase(BaseModel):
    name: str
    city: str
    total_capacity: int
    address: str


class VenueCreate(VenueBase):
    pass


class VenueResponse(VenueBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
