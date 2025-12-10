from fastapi import HTTPException, status

class RecordLockedException(HTTPException):
    def __init__(self, entity_type: str, entity_id: int, locked_by: str):
        super().__init__(
            status_code=status.HTTP_423_LOCKED,
            detail=f"{entity_type} заблокирован пользователем {locked_by}"
        )

class PermissionDeniedException(HTTPException):
    def __init__(self, message: str = "Недостаточно прав"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=message)

class NotAuthenticatedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не авторизован",
            headers={"WWW-Authenticate": "Bearer"}
        )

class ResourceNotFoundException(HTTPException):
    def __init__(self, entity_type: str, entity_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity_type} не найден"
        )
