from pydantic import BaseModel

class SupportCreate(BaseModel):
    subject: str
    message: str

class SupportResponse(BaseModel):
    message: str
    status: str = "open"

class SupportStatusUpdate(BaseModel):
    status: str