from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from app.db.models import AuditLog
from datetime import datetime

class AuditService:
    @staticmethod
    def log_action(db: Session, user_id: int, action: str, entity_type: str, entity_id: int,
                  old_values: Optional[Dict[str, Any]] = None, new_values: Optional[Dict[str, Any]] = None,
                  ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> AuditLog:
        log = AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            old_values=old_values,
            new_values=new_values,
            timestamp=datetime.utcnow(),
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    def get_entity_history(db: Session, entity_type: str, entity_id: int, limit: int = 50) -> list[AuditLog]:
        return db.query(AuditLog).filter(
            AuditLog.entity_type == entity_type,
            AuditLog.entity_id == entity_id
        ).order_by(AuditLog.timestamp.desc()).limit(limit).all()

audit_service = AuditService()
