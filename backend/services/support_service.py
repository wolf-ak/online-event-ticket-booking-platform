from sqlalchemy.orm import Session

from backend.models.support import SupportCase
from backend.schemas.support_schema import SupportCreate


def create_support_case(data: SupportCreate, user_id: int, db: Session):
    case = SupportCase(
        user_id=user_id,
        subject=data.subject,
        message=data.message,
        status="open"
    )

    db.add(case)
    db.commit()
    db.refresh(case)
    return case


def get_user_support_cases(user_id: int, db: Session):
    return db.query(SupportCase).filter(SupportCase.user_id == user_id).all()


def get_all_support_cases(db: Session):
    return db.query(SupportCase).all()


def update_support_status(case_id: int, status: str, db: Session) -> bool:
    case = db.query(SupportCase).filter(SupportCase.id == case_id).first()
    if not case:
        return False

    case.status = status
    db.commit()
    return True
