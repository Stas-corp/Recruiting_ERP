from typing import Optional, List

from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload

from app.db.models import Response
from app.crud.base import CRUDBase
from app.core.constants import ResponseStatusEnum
from app.schemas.response import ResponseCreate, ResponseUpdate

class CRUDResponse(CRUDBase[Response, ResponseCreate, ResponseUpdate]):
    def get_by_candidate_and_vacancy(
        self, 
        db: Session, 
        candidate_id: int, 
        vacancy_id: int
    ) -> Optional[Response]:
        return db.query(Response).filter(
            and_(Response.candidate_id == candidate_id, Response.vacancy_id == vacancy_id)
        ).first()


    def get_by_status(
        self, 
        db: Session, 
        status: ResponseStatusEnum, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Response]:
        return db.query(Response).filter(Response.status == status).offset(skip).limit(limit).all()


    def get_multi(self, db: Session, skip=0, limit=100):
        return (
            db.query(Response)
            .options(
                joinedload(Response.candidate),
                joinedload(Response.vacancy),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

crud_response = CRUDResponse(Response)
