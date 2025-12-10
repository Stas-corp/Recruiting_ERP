from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.common import PaginatedResponse
from app.crud.user import crud_user
from app.api.dependencies import get_current_user, check_permission

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[UserResponse])
def list_users(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000),
              db: Session = Depends(get_db), current_user: User = Depends(check_permission("manage_users"))):
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    total = crud_user.get_count(db)
    return {"total": total, "skip": skip, "limit": limit, "items": users}

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db),
            current_user: User = Depends(check_permission("manage_users"))):
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return user
