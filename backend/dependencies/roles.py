from fastapi import Depends, HTTPException, status

from backend.dependencies.get_current_user import get_current_user


def require_roles(*roles):
    def _role_guard(current_user = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user

    return _role_guard
