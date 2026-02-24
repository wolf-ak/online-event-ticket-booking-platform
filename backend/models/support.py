from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.sql import func
from backend.database import Base


class SupportCase(Base):
    __tablename__ = "support_cases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String(150), nullable=False)
    message = Column(String(255), nullable=False)
    status = Column(String(20), default="open")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
