from sqlalchemy.orm import Session
from passlib.context import CryptContext
from backend.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_user(user_data, db: Session):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        return None
    
    hashed_password = pwd_context.hash(user_data.password)
    # Defaulting to customer if not explicitly provided
    role = getattr(user_data, 'role', 'customer') 
    
    new_user = User(
        name=user_data.name, 
        email=user_data.email, 
        password_hash=hashed_password, 
        role=role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.password_hash):
        return None
    return user