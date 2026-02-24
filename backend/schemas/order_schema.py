from pydantic import BaseModel
from datetime import datetime
from typing import List


class OrderCreate(BaseModel):
    event_id: int
    seat_ids: List[int]
    payment_mode: str


class OrderResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    total_amount: int
    payment_mode: str
    order_status: str
    booking_time: datetime

    class Config:
        from_attributes = True
