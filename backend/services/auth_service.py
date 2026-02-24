from sqlalchemy.orm import Session

from backend.models.user import User
from backend.schemas.user_schema import UserCreate
from backend.utils.hash import hash_password, verify_password


def register_user(user: UserCreate, db: Session):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        return None

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user
