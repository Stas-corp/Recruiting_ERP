from app.crud.base import CRUDBase
from app.crud.candidate import crud_candidate
from app.crud.response import crud_response
from app.crud.user import crud_user
from app.crud.vacancy import crud_vacancy

__all__ = ["CRUDBase", "crud_candidate", "crud_response", "crud_user", "crud_vacancy"]
