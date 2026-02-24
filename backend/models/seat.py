from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from backend.database import Base

class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    seat_number = Column(String(10), nullable=False)
    status = Column(String(20), default="available")

    __table_args__ = (
        UniqueConstraint("event_id", "seat_number", name="unique_seat_per_event"),
    )