from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.core.security import decode_token
from app.core.exceptions import NotAuthenticatedException

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    token = credentials.credentials
    payload = decode_token(token)
    
    if not payload:
        raise NotAuthenticatedException()
    
    user_id = payload.get("sub")
    if not user_id:
        raise NotAuthenticatedException()
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise NotAuthenticatedException()
    
    return user

def check_permission(permission: str):
    def _check(user: User = Depends(get_current_user)) -> User:
        if "*" in user.role.permissions or permission in user.role.permissions:
            return user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    return _check
