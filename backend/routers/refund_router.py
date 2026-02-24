from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.dependencies.get_db import get_db
from backend.dependencies.get_current_user import get_current_user
from backend.dependencies.roles import require_roles

from backend.schemas.refund_schema import (
    RefundCreate,
    RefundResponse,
    RefundStatusUpdate
)

from backend.services.refund_service import (
    create_refund_request,
    get_all_refunds,
    update_refund_status,
    get_user_refunds
)

router = APIRouter(
    prefix="/refunds",
    tags=["Refunds"]
)


# -----------------------------------
# Customer: Request Refund
# -----------------------------------
@router.post("/", response_model=RefundResponse)
def request_refund(
    data: RefundCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("customer"))
):
    refund = create_refund_request(data, current_user.id, db)

    if not refund:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refund not allowed (event passed or invalid order)"
        )

    return refund


# -----------------------------------
# Customer: View My Refund Requests
# -----------------------------------
@router.get("/my", response_model=List[RefundResponse])
def my_refunds(
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("customer"))
):
    return get_user_refunds(current_user.id, db)


# -----------------------------------
# Admin/Support: View All Refund Requests
# -----------------------------------
@router.get("/", response_model=List[RefundResponse])
def all_refunds(
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("admin", "support"))
):
    return get_all_refunds(db)


# -----------------------------------
# Admin/Support: Approve / Reject Refund
# -----------------------------------
@router.patch("/{refund_id}")
def update_refund(
    refund_id: int,
    data: RefundStatusUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("admin", "support"))
):
    updated = update_refund_status(refund_id, data.status, db)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refund request not found"
        )

    return {"message": f"Refund {data.status} successfully"}
