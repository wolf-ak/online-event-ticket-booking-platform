from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SupportCreate(BaseModel):
    subject: str
    message: str

class SupportResponse(BaseModel):
    id: Optional[int] = None
    subject: Optional[str] = None
    message: str
    status: str = "open"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SupportStatusUpdate(BaseModel):
    status: str
