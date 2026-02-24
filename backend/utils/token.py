from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError

from backend.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
    to_encode = data.copy()

    expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
    if expires_delta is not None:
        expire_minutes = expires_delta

    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
