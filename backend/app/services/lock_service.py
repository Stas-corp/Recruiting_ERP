from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from app.db.models import EditLock, User
from app.config import settings
from app.core.exceptions import RecordLockedException

class LockService:
    @staticmethod
    def acquire_lock(
        db: Session, 
        entity_type: str, 
        entity_id: int, 
        user_id: int,
        candidate_id: Optional[int] = None, 
        response_id: Optional[int] = None
    ) -> EditLock:
        existing_lock = db.query(EditLock).filter(
            EditLock.entity_type == entity_type,
            (EditLock.candidate_id == candidate_id) if entity_type == "candidate" else (EditLock.response_id == response_id)
        ).first()
        
        if existing_lock and existing_lock.locked_by_id != user_id:
            locked_user = db.query(User).filter(User.id == existing_lock.locked_by_id).first()
            raise RecordLockedException(entity_type, entity_id, locked_user.full_name if locked_user else "Unknown")
        
        if existing_lock and existing_lock.expires_at < datetime.utcnow():
            db.delete(existing_lock)
            db.commit()
        else:
            return existing_lock
        
        lock = EditLock(
            entity_type=entity_type,
            candidate_id=candidate_id if entity_type == "candidate" else None,
            response_id=response_id if entity_type == "response" else None,
            locked_by_id=user_id,
            expires_at=datetime.utcnow() + timedelta(minutes=settings.EDIT_LOCK_TIMEOUT_MINUTES)
        )
        db.add(lock)
        db.commit()
        db.refresh(lock)
        return lock

    @staticmethod
    def release_lock(
        db: Session, 
        entity_type: str, 
        entity_id: int, 
        user_id: int
    ) -> bool:
        lock = db.query(EditLock).filter(EditLock.entity_type == entity_type).first()
        if lock and lock.locked_by_id == user_id:
            db.delete(lock)
            db.commit()
            return True
        return False

    @staticmethod
    def cleanup_expired_locks(db: Session):
        db.query(EditLock).filter(EditLock.expires_at < datetime.utcnow()).delete()
        db.commit()

lock_service = LockService()
