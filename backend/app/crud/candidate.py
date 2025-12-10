from sqlalchemy.orm import Session
from sqlalchemy import or_, func, select
from typing import Optional, List, Tuple
from app.db.models import Candidate
from app.schemas.candidate import CandidateCreate, CandidateUpdate
from app.crud.base import CRUDBase

class CRUDCandidate(CRUDBase[Candidate, CandidateCreate, CandidateUpdate]):
    def search(self, db: Session, query: str, skip: int = 0, limit: int = 100) -> Tuple[List[Candidate], int]:
        search_query = f"%{query}%"
        items = db.query(Candidate).where(
            or_(
                Candidate.full_name.ilike(search_query),
                Candidate.email.ilike(search_query),
                Candidate.phone.ilike(search_query)
            )
        ).offset(skip).limit(limit).all()
        
        total = db.query(func.count(Candidate.id)).where(
            or_(
                Candidate.full_name.ilike(search_query),
                Candidate.email.ilike(search_query),
                Candidate.phone.ilike(search_query)
            )
        ).scalar()
        return items, total

    def get_by_email(self, db: Session, email: str) -> Optional[Candidate]:
        return db.query(Candidate).filter(Candidate.email == email).first()

crud_candidate = CRUDCandidate(Candidate)
