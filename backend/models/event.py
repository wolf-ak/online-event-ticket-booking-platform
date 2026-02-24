from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from backend.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(String(255))
    category = Column(String(50), nullable=False)  
    event_date = Column(DateTime, nullable=False)
    ticket_price = Column(Integer, nullable=False)
    
    max_tickets_per_user = Column(Integer, default=5, nullable=False) 
    status = Column(String(20), default="upcoming") 

    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())