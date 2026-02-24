from pydantic import BaseModel

class RefundCreate(BaseModel):
    order_id: int
    reason: str

class RefundResponse(BaseModel):
    id: Optional[int] = None
    order_id: int
    status: str = "pending"
    message: str

class RefundStatusUpdate(BaseModel):
    status: str