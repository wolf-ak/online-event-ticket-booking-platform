from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.dependencies.get_db import get_db
from backend.dependencies.get_current_user import get_current_user

from backend.schemas.ticket_schema import TicketResponse

from backend.services.ticket_service import (
    get_user_tickets,
    get_ticket_by_id,
    validate_ticket_entry
)

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


# -----------------------------------
# Customer: View My Tickets
# -----------------------------------
@router.get("/my", response_model=List[TicketResponse])
def my_tickets(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_user_tickets(current_user.id, db)


# -----------------------------------
# Get Single Ticket Details
# -----------------------------------
@router.get("/{ticket_id}", response_model=TicketResponse)
def ticket_details(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    ticket = get_ticket_by_id(ticket_id, current_user.id, db)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    return ticket


# -----------------------------------
# Entry Manager: Validate Ticket
# -----------------------------------
@router.post("/{ticket_id}/validate")
def validate_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):  
    if current_user.role not in ["admin", "entry_manager"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only entry managers can validate tickets")
    
    result = validate_ticket_entry(ticket_id, current_user.id, db)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or already used ticket"
        )

    return {"message": "Ticket validated successfully"}