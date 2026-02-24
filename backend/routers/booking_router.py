from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.dependencies.get_db import get_db
from backend.dependencies.get_current_user import get_current_user
from backend.schemas.order_schema import OrderCreate, OrderResponse
from backend.services.booking_service import (
    list_events,
    get_event_seats,
    create_order,
    process_payment,
    get_user_orders
)

router = APIRouter(
    prefix="/booking",
    tags=["Booking"]
)


# -----------------------------------
# Get All Available Events
# -----------------------------------
@router.get("/events")
def get_events(db: Session = Depends(get_db)):
    return list_events(db)


# -----------------------------------
# Get Seats for an Event
# -----------------------------------
@router.get("/events/{event_id}/seats")
def get_seats(event_id: int, db: Session = Depends(get_db)):
    return get_event_seats(event_id, db)


# -----------------------------------
# Create Order (Seat Lock Happens in Service)
# -----------------------------------
@router.post("/orders", response_model=OrderResponse)
def book_tickets(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    created_order = create_order(order, current_user.id, db)

    if not created_order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seats unavailable or booking limit exceeded"
        )

    return created_order


# -----------------------------------
# Process Payment
# -----------------------------------
@router.post("/orders/{order_id}/pay")
def pay_for_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = process_payment(order_id, current_user.id, db)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment failed or invalid order"
        )

    return {"message": "Payment successful"}


# -----------------------------------
# View My Orders
# -----------------------------------
@router.get("/my-orders", response_model=List[OrderResponse])
def my_orders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_user_orders(current_user.id, db)