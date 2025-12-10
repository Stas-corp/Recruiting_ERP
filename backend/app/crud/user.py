from sqlalchemy.orm import Session
from typing import Optional
from app.db.models import User, Role
from app.schemas.user import UserCreate, UserUpdate
from app.crud.base import CRUDBase
from app.core.security import get_password_hash

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, obj_in: UserCreate) -> User:
        role = db.query(Role).filter(Role.name == obj_in.role).first()
        db_obj = User(
            email=obj_in.email,
            password_hash=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            role_id=role.id if role else 1
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

crud_user = CRUDUser(User)
