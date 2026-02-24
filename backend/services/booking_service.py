from typing import List, Optional

from sqlalchemy.orm import Session

from backend.models.event import Event
from backend.models.seat import Seat
from backend.models.order import Order
from backend.models.order_seat import OrderSeat
from backend.models.ticket import Ticket
from backend.schemas.oder_schema import OrderCreate


def list_events(db: Session):
    return db.query(Event).all()


def get_event_seats(event_id: int, db: Session):
    return db.query(Seat).filter(Seat.event_id == event_id).all()


def _count_user_event_seats(user_id: int, event_id: int, db: Session) -> int:
    orders = db.query(Order).filter(
        Order.user_id == user_id,
        Order.event_id == event_id
    ).all()

    total = 0
    for order in orders:
        total += db.query(OrderSeat).filter(OrderSeat.order_id == order.id).count()

    return total


def create_order(data: OrderCreate, user_id: int, db: Session) -> Optional[Order]:
    event = db.query(Event).filter(Event.id == data.event_id).first()
    if not event:
        return None

    if event.status != "upcoming":
        return None

    seat_ids = data.seat_ids
    if not seat_ids:
        return None

    if len(seat_ids) > event.max_tickets_per_user:
        return None

    existing_count = _count_user_event_seats(user_id, data.event_id, db)
    if existing_count + len(seat_ids) > event.max_tickets_per_user:
        return None

    seats = db.query(Seat).filter(
        Seat.id.in_(seat_ids),
        Seat.event_id == data.event_id
    ).all()

    if len(seats) != len(seat_ids):
        return None

    for seat in seats:
        if seat.status != "available":
            return None

    for seat in seats:
        seat.status = "reserved"

    order = Order(
        user_id=user_id,
        event_id=data.event_id,
        total_amount=event.ticket_price * len(seats),
        payment_mode=data.payment_mode,
        order_status="pending"
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    for seat in seats:
        link = OrderSeat(order_id=order.id, seat_id=seat.id)
        db.add(link)

    db.commit()
    return order


def process_payment(order_id: int, user_id: int, db: Session) -> bool:
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()

    if not order:
        return False

    if order.order_status != "pending":
        return False

    order_seats = db.query(OrderSeat).filter(OrderSeat.order_id == order.id).all()
    if not order_seats:
        return False

    for order_seat in order_seats:
        seat = db.query(Seat).filter(Seat.id == order_seat.seat_id).first()
        if seat:
            seat.status = "booked"

        ticket = Ticket(order_id=order.id, seat_id=order_seat.seat_id, status="valid")
        db.add(ticket)

    order.order_status = "confirmed"
    db.commit()
    return True


def get_user_orders(user_id: int, db: Session):
    return db.query(Order).filter(Order.user_id == user_id).all()
