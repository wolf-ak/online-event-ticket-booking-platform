import bcrypt

def hash_password(password: str) -> str:
    """Hash password using bcrypt, truncating to 72 bytes if necessary."""
    # bcrypt only supports 72 bytes, so truncate if needed
    password_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash using bcrypt."""
    # Truncate to 72 bytes to match hash_password behavior
    password_bytes = plain_password.encode("utf-8")[:72]
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)
