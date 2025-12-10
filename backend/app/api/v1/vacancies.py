from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.schemas.vacancy import VacancyCreate, VacancyUpdate, VacancyResponse
from app.schemas.common import PaginatedResponse
from app.crud.vacancy import crud_vacancy
from app.api.dependencies import get_current_user
from app.services.audit_service import audit_service

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[VacancyResponse])
def list_vacancies(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000),
                  db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    vacancies = crud_vacancy.get_multi(db, skip=skip, limit=limit)
    total = crud_vacancy.get_count(db)
    return {"total": total, "skip": skip, "limit": limit, "items": vacancies}

@router.get("/{vacancy_id}", response_model=VacancyResponse)
def get_vacancy(vacancy_id: int, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    vacancy = crud_vacancy.get(db, id=vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена")
    return vacancy

@router.post("/", response_model=VacancyResponse)
def create_vacancy(vacancy_in: VacancyCreate, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    vacancy = crud_vacancy.create(db, obj_in=vacancy_in)
    audit_service.log_action(db, user_id=current_user.id, action="create", entity_type="vacancy",
                            entity_id=vacancy.id, new_values=vacancy_in.dict())
    return vacancy

@router.patch("/{vacancy_id}", response_model=VacancyResponse)
def update_vacancy(vacancy_id: int, vacancy_in: VacancyUpdate, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    vacancy = crud_vacancy.get(db, id=vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена")
    vacancy = crud_vacancy.update(db, db_obj=vacancy, obj_in=vacancy_in)
    audit_service.log_action(db, user_id=current_user.id, action="update", entity_type="vacancy",
                            entity_id=vacancy.id, new_values=vacancy_in.dict(exclude_unset=True))
    return vacancy

@router.delete("/{vacancy_id}")
def delete_vacancy(vacancy_id: int, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    vacancy = crud_vacancy.get(db, id=vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена")
    crud_vacancy.delete(db, id=vacancy_id)
    audit_service.log_action(db, user_id=current_user.id, action="delete", entity_type="vacancy",
                            entity_id=vacancy_id)
    return {"status": "deleted"}
