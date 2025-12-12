from typing import Dict, Any

from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.db.session import get_db
from app.db.models import User, Response
from app.api.dependencies import get_current_user

router = APIRouter()


@router.get("/overview")
def get_analytics_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    total_responses = db.query(func.count(Response.id)).scalar()
    status_breakdown = db.query(Response.status, func.count(Response.id).label("count")).group_by(Response.status).all()
    source_breakdown = db.query(Response.source, func.count(Response.id).label("count")).group_by(Response.source).all()
    
    return {
        "total_responses": total_responses,
        "status_breakdown": [{"status": s[0], "count": s[1]} for s in status_breakdown],
        "source_breakdown": [{"source": s[0], "count": s[1]} for s in source_breakdown],
    }
