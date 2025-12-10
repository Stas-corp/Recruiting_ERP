from app.db.models import Vacancy
from app.schemas.vacancy import VacancyCreate, VacancyUpdate
from app.crud.base import CRUDBase

class CRUDVacancy(CRUDBase[Vacancy, VacancyCreate, VacancyUpdate]):
    pass

crud_vacancy = CRUDVacancy(Vacancy)
