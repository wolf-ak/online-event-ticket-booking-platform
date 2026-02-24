from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Session

from backend.models.refund import RefundRequest
from backend.models.order import Order
from backend.models.order_seat import OrderSeat
from backend.models.seat import Seat
from backend.models.ticket import Ticket
from backend.models.event import Event
from backend.schemas.refund_schema import RefundCreate


def create_refund_request(data: RefundCreate, user_id: int, db: Session):
    order = db.query(Order).filter(
        Order.id == data.order_id,
        Order.user_id == user_id
    ).first()

    if not order:
        return None

    event = db.query(Event).filter(Event.id == order.event_id).first()
    if not event:
        return None

    if event.event_date <= datetime.utcnow():
        return None

    existing = db.query(RefundRequest).filter(
        RefundRequest.order_id == data.order_id,
        RefundRequest.user_id == user_id
    ).first()
    if existing:
        return existing

    refund = RefundRequest(
        order_id=data.order_id,
        user_id=user_id,
        reason=data.reason,
        message=data.reason,
        status="pending"
    )

    db.add(refund)
    db.commit()
    db.refresh(refund)
    return refund


def get_all_refunds(db: Session):
    return db.query(RefundRequest).all()


def update_refund_status(refund_id: int, status: str, db: Session) -> bool:
    refund = db.query(RefundRequest).filter(RefundRequest.id == refund_id).first()
    if not refund:
        return False

    refund.status = status

    if status == "approved":
        order = db.query(Order).filter(Order.id == refund.order_id).first()
        if order:
            order.order_status = "refunded"

            order_seats = db.query(OrderSeat).filter(
                OrderSeat.order_id == order.id
            ).all()

            for order_seat in order_seats:
                seat = db.query(Seat).filter(Seat.id == order_seat.seat_id).first()
                if seat:
                    seat.status = "available"

                ticket = db.query(Ticket).filter(
                    Ticket.order_id == order.id,
                    Ticket.seat_id == order_seat.seat_id
                ).first()
                if ticket:
                    ticket.status = "refunded"

    db.commit()
    return True


def get_user_refunds(user_id: int, db: Session):
    return db.query(RefundRequest).filter(RefundRequest.user_id == user_id).all()
