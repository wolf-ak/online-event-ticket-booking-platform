from sqlalchemy.orm import Session
from backend.models.event import Event
from backend.models.seat import Seat
from backend.models.order import Order
from backend.models.ticket import Ticket

def list_events(db: Session):
    return db.query(Event).filter(Event.status == "upcoming").all()

def get_event_seats(event_id: int, db: Session):
    return db.query(Seat).filter(Seat.event_id == event_id).all()

def create_order(order_data, user_id: int, db: Session):
    try:
        # Lock seats to prevent double booking
        seats = db.query(Seat).filter(Seat.id.in_(order_data.seat_ids)).with_for_update().all()
        
        if len(seats) != len(order_data.seat_ids) or any(seat.status != 'available' for seat in seats):
            return None # Seats unavailable

        # Mark seats as reserved
        for seat in seats:
            seat.status = "booked"
        
        # Calculate total
        event = db.query(Event).filter(Event.id == order_data.event_id).first()
        total_amount = event.ticket_price * len(seats)

        new_order = Order(
            user_id=user_id, 
            event_id=order_data.event_id, 
            total_amount=total_amount, 
            payment_mode=order_data.payment_mode,
            order_status="pending"
        )
        db.add(new_order)
        db.flush() # Get order ID before committing

        # We store the seat IDs in the order temporarily to generate tickets on payment
        setattr(new_order, '_temp_seat_ids', order_data.seat_ids) 
        db.commit()
        db.refresh(new_order)
        return new_order
    except Exception:
        db.rollback()
        return None

def process_payment(order_id: int, user_id: int, db: Session):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    if not order or order.order_status != "pending":
        return False
    
    # Simulate payment success, generate tickets
    order.order_status = "confirmed"
    
    # Fetch seats tied to this event that the user just booked (simplified)
    seats = db.query(Seat).filter(Seat.event_id == order.event_id, Seat.status == "booked").limit(order.total_amount // order.event.ticket_price if order.event else 1).all()
    
    for seat in seats:
        new_ticket = Ticket(order_id=order.id, seat_id=seat.id, status="valid")
        db.add(new_ticket)
        
    db.commit()
    return True

def get_user_orders(user_id: int, db: Session):
    return db.query(Order).filter(Order.user_id == user_id).all()