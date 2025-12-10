from pydantic import BaseModel
from typing import Optional, Generic, TypeVar
from datetime import datetime

T = TypeVar("T")

class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 100

class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    skip: int
    limit: int
    items: list[T]

class TimestampBase(BaseModel):
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
