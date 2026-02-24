from pydantic import BaseModel

class TicketResponse(BaseModel):
    id: int
    order_id: int
    seat_id: int
    status: str

    class Config:
        from_attributes = True