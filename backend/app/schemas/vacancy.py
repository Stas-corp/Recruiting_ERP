from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.common import TimestampBase

class VacancyCreate(BaseModel):
    position: str = Field(..., min_length=2)
    department: str = Field(..., min_length=2)
    city: str = Field(..., min_length=2)
    grade: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    description: Optional[str] = None

class VacancyUpdate(BaseModel):
    position: Optional[str] = None
    department: Optional[str] = None
    city: Optional[str] = None
    grade: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class VacancyResponse(TimestampBase):
    id: int
    position: str
    department: str
    city: str
    grade: Optional[str]
    salary_min: Optional[int]
    salary_max: Optional[int]
    description: Optional[str]
    is_active: bool
    class Config:
        from_attributes = True
