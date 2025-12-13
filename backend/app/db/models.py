from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, 
    ForeignKey, JSON, Enum as SQLEnum, UniqueConstraint, Index
)

from app.db.base import Base, TimestampMixin
from app.core.constants import ResponseStatusEnum, ResponseSourceEnum, RoleEnum


class Role(Base, TimestampMixin):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(SQLEnum(RoleEnum), unique=True, nullable=False, index=True)
    description = Column(String(255))
    permissions = Column(JSON, default=list)
    
    users = relationship("User", back_populates="role")


class User(Base, TimestampMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    
    role = relationship("Role", back_populates="users")
    responses_assigned = relationship("Response", back_populates="assigned_recruiter")
    edit_locks = relationship("EditLock", back_populates="locked_by")
    audit_logs = relationship("AuditLog", back_populates="user")


class Candidate(Base, TimestampMixin):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False, index=True)
    phone = Column(String(20), index=True)
    email = Column(String(255), index=True)
    resume = Column(Text)
    skills = Column(JSON, default=list)
    experience = Column(Text)
    notes = Column(Text)
    
    responses = relationship("Response", back_populates="candidate", cascade="all, delete-orphan")
    edit_locks = relationship("EditLock", back_populates="candidate")


class Vacancy(Base, TimestampMixin):
    __tablename__ = "vacancies"
    id = Column(Integer, primary_key=True, index=True)
    position = Column(String(255), nullable=False, index=True)
    department = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False, index=True)
    grade = Column(String(50))
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    description = Column(Text)
    is_active = Column(Boolean, default=True, index=True)
    
    responses = relationship("Response", back_populates="vacancy", cascade="all, delete-orphan")


class Response(Base, TimestampMixin):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False, index=True)
    vacancy_id = Column(Integer, ForeignKey("vacancies.id"), nullable=False, index=True)
    source = Column(SQLEnum(ResponseSourceEnum), nullable=False, index=True)
    status = Column(SQLEnum(ResponseStatusEnum), default=ResponseStatusEnum.NEW, nullable=False, index=True)
    response_date = Column(DateTime, default=datetime.utcnow)
    assigned_recruiter_id = Column(Integer, ForeignKey("users.id"))
    external_id = Column(String(255))
    
    candidate = relationship("Candidate", back_populates="responses")
    vacancy = relationship("Vacancy", back_populates="responses")
    assigned_recruiter = relationship("User", back_populates="responses_assigned", foreign_keys=[assigned_recruiter_id])
    status_history = relationship("ResponseStatusHistory", back_populates="response", cascade="all, delete-orphan")
    edit_locks = relationship("EditLock", back_populates="response")
    
    __table_args__ = (
        UniqueConstraint("candidate_id", "vacancy_id", "source", name="uq_candidate_vacancy_source"),
    )


class ResponseStatusHistory(Base, TimestampMixin):
    __tablename__ = "response_status_history"
    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey("responses.id"), nullable=False, index=True)
    old_status = Column(SQLEnum(ResponseStatusEnum))
    new_status = Column(SQLEnum(ResponseStatusEnum), nullable=False)
    changed_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    changed_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    comment = Column(Text)
    
    response = relationship("Response", back_populates="status_history")
    changed_by = relationship("User")


class EditLock(Base):
    __tablename__ = "edit_locks"
    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(50), nullable=False, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), index=True)
    response_id = Column(Integer, ForeignKey("responses.id"), index=True)
    locked_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    locked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False, index=True)
    
    locked_by = relationship("User", back_populates="edit_locks")
    candidate = relationship("Candidate", back_populates="edit_locks")
    response = relationship("Response", back_populates="edit_locks")
    
    __table_args__ = (
        UniqueConstraint("entity_type", "candidate_id", "response_id", name="uq_single_lock_per_entity"),
    )


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    action = Column(String(50), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False, index=True)
    entity_id = Column(Integer, nullable=False, index=True)
    old_values = Column(JSON)
    new_values = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    ip_address = Column(String(50))
    user_agent = Column(String(500))
    
    user = relationship("User", back_populates="audit_logs")
