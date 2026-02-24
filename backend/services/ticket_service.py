from sqlalchemy.orm import Session

from backend.models.ticket import Ticket
from backend.models.order import Order


def get_user_tickets(user_id: int, db: Session):
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    order_ids = [o.id for o in orders]

    if not order_ids:
        return []

    return db.query(Ticket).filter(Ticket.order_id.in_(order_ids)).all()


def get_ticket_by_id(ticket_id: int, user_id: int, db: Session):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        return None

    order = db.query(Order).filter(Order.id == ticket.order_id).first()
    if not order or order.user_id != user_id:
        return None

    return ticket


def validate_ticket_entry(ticket_id: int, user_id: int, db: Session) -> bool:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        return False

    if ticket.status != "valid":
        return False

    ticket.status = "used"
    db.commit()
    return True
