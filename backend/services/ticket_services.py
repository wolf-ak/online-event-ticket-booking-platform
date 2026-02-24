from sqlalchemy.orm import Session
from backend.models.ticket import Ticket

def get_user_tickets(user_id: int, db: Session):
    # Simplification: Join with Order to verify user
    from backend.models.order import Order
    return db.query(Ticket).join(Order).filter(Order.user_id == user_id).all()

def get_ticket_by_id(ticket_id: int, user_id: int, db: Session):
    from backend.models.order import Order
    return db.query(Ticket).join(Order).filter(Ticket.id == ticket_id, Order.user_id == user_id).first()

def validate_ticket_entry(ticket_id: int, manager_id: int, db: Session):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket or ticket.status != "valid":
        return False
    
    ticket.status = "used"
    db.commit()
    return True