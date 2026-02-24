from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.dependencies.get_db import get_db
from backend.dependencies.get_current_user import get_current_user

from backend.schemas.support_schema import (
    SupportCreate,
    SupportResponse,
    SupportStatusUpdate
)

from backend.services.support_service import (
    create_support_case,
    get_user_support_cases,
    get_all_support_cases,
    update_support_status
)

router = APIRouter(
    prefix="/support",
    tags=["Support"]
)


# -----------------------------------
# Customer: Create Support Case
# -----------------------------------
@router.post("/", response_model=SupportResponse)
def create_case(
    data: SupportCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_support_case(data, current_user.id, db)


# -----------------------------------
# Customer: View My Support Cases
# -----------------------------------
@router.get("/my", response_model=List[SupportResponse])
def my_cases(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_user_support_cases(current_user.id, db)


# -----------------------------------
# Admin/Support: View All Support Cases
# -----------------------------------
@router.get("/", response_model=List[SupportResponse])
def all_cases(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_all_support_cases(db)


# -----------------------------------
# Admin/Support: Update Case Status
# -----------------------------------
@router.patch("/{case_id}")
def update_case_status(
    case_id: int,
    data: SupportStatusUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    updated = update_support_status(case_id, data.status, db)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Support case not found"
        )

    return {"message": f"Support case {data.status} successfully"}