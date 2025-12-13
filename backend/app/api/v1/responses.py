from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.db.session import get_db
from app.crud.response import crud_response
from app.schemas.common import PaginatedResponse
from app.api.dependencies import get_current_user
from app.core.constants import ResponseStatusEnum
from app.services.lock_service import lock_service
from app.services.audit_service import audit_service
from app.db.models import User, Response, ResponseStatusHistory, EditLock
from app.schemas.response import ResponseCreate, ResponseStatusChange, ResponseResponse
from app.services.notification_service import NotificationService, ConsoleNotificationProvider

router = APIRouter()
notification_service = NotificationService(ConsoleNotificationProvider())


@router.get("/", response_model=PaginatedResponse[ResponseResponse])
def list_responses(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    responses = crud_response.get_multi(db, skip=skip, limit=limit)
    total = crud_response.get_count(db)
    return {
        "total": total, 
        "skip": skip, 
        "limit": limit, 
        "items": responses
    }


@router.get("/{response_id}", response_model=ResponseResponse)
def get_response(
    response_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    response = crud_response.get(
        db, 
        id=response_id
    )
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Отклик не найден")
    
    lock_service.acquire_lock(
        db, 
        entity_type="response", 
        entity_id=response_id,
        user_id=current_user.id, 
        response_id=response_id
    )
    
    return response


@router.post("/", response_model=ResponseResponse)
def create_response(
    response_in: ResponseCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    response = crud_response.create(
        db, 
        obj_in=response_in
    )
    
    audit_service.log_action(
        db, 
        user_id=current_user.id, 
        action="create", 
        entity_type="response",
        entity_id=response.id, 
        new_values=response_in.dict()
    )
    
    return response


@router.patch("/{response_id}/status", response_model=ResponseResponse)
def change_response_status(
    response_id: int, 
    status_change: ResponseStatusChange,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    response = crud_response.get(
        db, 
        id=response_id
    )
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Отклик не найден")
    
    lock = db.query(EditLock).filter(EditLock.response_id == response_id).first()
    if lock and lock.locked_by_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="Отклик заблокирован")
    
    old_status = response.status
    response.status = status_change.new_status
    db.add(response)
    
    status_history = ResponseStatusHistory(
        response_id=response.id, 
        old_status=old_status, 
        new_status=status_change.new_status,
        changed_by_id=current_user.id, 
        changed_at=datetime.utcnow(), 
        comment=status_change.comment
    )
    
    db.add(status_history)
    db.commit()
    db.refresh(response)
    
    audit_service.log_action(
        db, 
        user_id=current_user.id, 
        action="status_change", 
        entity_type="response",
        entity_id=response.id, 
        old_values={
            "status": str(old_status)
        },
        new_values={
            "status": str(status_change.new_status)
        }
    )
    
    if status_change.new_status == ResponseStatusEnum.IN_FORCE:
        notification_service.notify_candidate_confirmed(
            response.candidate.full_name,
            response.vacancy.position, 
            str(current_user.id)
        )
    
    return response


@router.post("/{response_id}/unlock")
def unlock_response(
    response_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    lock_service.release_lock(
        db, 
        entity_type="response", 
        entity_id=response_id, 
        user_id=current_user.id
    )
    
    return {"status": "unlocked"}
