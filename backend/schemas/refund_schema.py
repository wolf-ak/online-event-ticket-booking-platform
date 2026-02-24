from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RefundCreate(BaseModel):
    order_id: int
    reason: str

class RefundResponse(BaseModel):
    id: Optional[int] = None
    order_id: int
    status: str = "pending"
    message: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RefundStatusUpdate(BaseModel):
    status: str
