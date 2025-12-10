from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from app.schemas.common import TimestampBase

class CandidateCreate(BaseModel):
    full_name: str = Field(..., min_length=2)
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    resume: Optional[str] = None
    skills: List[str] = []
    experience: Optional[str] = None
    notes: Optional[str] = None

class CandidateUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    resume: Optional[str] = None
    skills: Optional[List[str]] = None
    experience: Optional[str] = None
    notes: Optional[str] = None

class CandidateResponse(TimestampBase):
    id: int
    full_name: str
    phone: Optional[str]
    email: Optional[str]
    resume: Optional[str]
    skills: List[str]
    experience: Optional[str]
    notes: Optional[str]
    class Config:
        from_attributes = True

class CandidateDetailResponse(CandidateResponse):
    responses_count: int = 0
