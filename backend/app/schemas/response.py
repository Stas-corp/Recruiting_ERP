from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import TimestampBase
from app.schemas.vacancy import VacancyResponse
from app.schemas.candidate import CandidateResponse
from app.core.constants import ResponseStatusEnum, ResponseSourceEnum


class ResponseCreate(BaseModel):
    candidate_id: int
    vacancy_id: int
    source: ResponseSourceEnum
    response_date: Optional[datetime] = None
    assigned_recruiter_id: Optional[int] = None


class ResponseStatusChange(BaseModel):
    new_status: ResponseStatusEnum
    comment: Optional[str] = None


class ResponseStatusHistoryResponse(BaseModel):
    id: int
    old_status: Optional[ResponseStatusEnum]
    new_status: ResponseStatusEnum
    changed_by_id: int
    changed_at: datetime
    comment: Optional[str]
    class Config:
        from_attributes = True


class ResponseUpdate(BaseModel):
    assigned_recruiter_id: Optional[int] = None


class ResponseResponse(TimestampBase):
    id: int
    candidate: CandidateResponse
    vacancy: VacancyResponse
    source: ResponseSourceEnum
    status: ResponseStatusEnum
    response_date: datetime
    assigned_recruiter_id: Optional[int]
    class Config:
        from_attributes = True


class ResponseDetailResponse(ResponseResponse):
    status_history: list[ResponseStatusHistoryResponse] = []
    class Config:
        from_attributes = True
