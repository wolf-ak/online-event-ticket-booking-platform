from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from backend.database import Base


class OrderSeat(Base):
    __tablename__ = "order_seats"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("order_id", "seat_id", name="unique_order_seat"),
    )
