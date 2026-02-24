from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from backend.database import Base

class Venue(Base):
    __tablename__ = "venues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False) 
    total_capacity = Column(Integer, nullable=False) 
    address = Column(String(255), nullable=False) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())