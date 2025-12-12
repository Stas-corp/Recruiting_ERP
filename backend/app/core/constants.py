from enum import Enum

class ResponseStatusEnum(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    REJECTED = "rejected"
    AWAITING_DECISION = "awaiting_decision"
    PASSED_TO_MANAGER = "passed_to_manager"
    DOCUMENTATION = "documentation"
    IN_FORCE = "in_force"

class ResponseSourceEnum(str, Enum):
    WORK_UA = "work_ua"
    ROBOTA_UA = "robota_ua"
    OLX = "olx"
    WEBSITE = "website"

class RoleEnum(str, Enum):
    ADMIN = "admin"
    RECRUITER = "recruiter"
    INTERVIEWER = "interviewer"

class AuditActionEnum(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    STATUS_CHANGE = "status_change"

class PermissionEnum(str, Enum):
    VIEW_CANDIDATES = "view_candidates"
    EDIT_CANDIDATES = "edit_candidates"
    DELETE_CANDIDATES = "delete_candidates"
    VIEW_RESPONSES = "view_responses"
    CHANGE_RESPONSE_STATUS = "change_response_status"
    MANAGE_USERS = "manage_users"
    VIEW_AUDIT_LOGS = "view_audit_logs"
