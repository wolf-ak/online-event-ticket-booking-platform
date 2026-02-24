from pydantic import BaseModel

class SeatBase(BaseModel):
    seat_number: str
    status: str = "available"

class SeatCreate(SeatBase):
    pass

class SeatResponse(SeatBase):
    id: int
    event_id: int

    class Config:
        from_attributes = True