from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.db.models import User
from app.db.session import get_db
from app.crud.candidate import crud_candidate
from app.schemas.common import PaginatedResponse
from app.api.dependencies import get_current_user
from app.services.lock_service import lock_service
from app.services.audit_service import audit_service
from app.schemas.candidate import CandidateCreate, CandidateUpdate, CandidateResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[CandidateResponse])
def list_candidates(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    candidates = crud_candidate.get_multi(db, skip=skip, limit=limit)
    total = crud_candidate.get_count(db)
    return {
        "total": total, 
        "skip": skip, 
        "limit": limit, 
        "items": candidates
    }


@router.get("/search", response_model=PaginatedResponse[CandidateResponse])
def search_candidates(
    q: str = Query(..., min_length=2), 
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    items, total = crud_candidate.search(db, query=q, skip=skip, limit=limit)
    return {"total": total, "skip": skip, "limit": limit, "items": items}


@router.get("/{candidate_id}", response_model=CandidateResponse)
def get_candidate(
    candidate_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    candidate = crud_candidate.get(db, id=candidate_id)
    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Кандидат не найден")
    lock_service.acquire_lock(db, entity_type="candidate", entity_id=candidate_id,
                            user_id=current_user.id, candidate_id=candidate_id)
    return candidate


@router.post("/", response_model=CandidateResponse)
def create_candidate(
    candidate_in: CandidateCreate, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    candidate = crud_candidate.create(db, obj_in=candidate_in)
    audit_service.log_action(db, user_id=current_user.id, action="create", entity_type="candidate",
                            entity_id=candidate.id, new_values=candidate_in.dict())
    return candidate


@router.patch("/{candidate_id}", response_model=CandidateResponse)
def update_candidate(
    candidate_id: int, 
    candidate_in: CandidateUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    candidate = crud_candidate.get(db, id=candidate_id)
    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Кандидат не найден")
    candidate = crud_candidate.update(db, db_obj=candidate, obj_in=candidate_in)
    audit_service.log_action(db, user_id=current_user.id, action="update", entity_type="candidate",
                            entity_id=candidate.id, new_values=candidate_in.dict(exclude_unset=True))
    return candidate


@router.delete("/{candidate_id}")
def delete_candidate(
    candidate_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    candidate = crud_candidate.get(db, id=candidate_id)
    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Кандидат не найден")
    crud_candidate.delete(db, id=candidate_id)
    audit_service.log_action(db, user_id=current_user.id, action="delete", entity_type="candidate",
                            entity_id=candidate_id)
    return {"status": "deleted"}


@router.post("/{candidate_id}/unlock")
def unlock_candidate(
    candidate_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    lock_service.release_lock(db, entity_type="candidate", entity_id=candidate_id, user_id=current_user.id)
    return {"status": "unlocked"}
