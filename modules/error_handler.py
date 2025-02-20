from typing import Dict, Any, Optional

class TodoError(Exception):
    """Base exception class for Todo List application."""
    def __init__(self, message: str, error_code: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

class TaskNotFoundError(TodoError):
    """Raised when a task with specified ID is not found."""
    def __init__(self, task_id: int):
        super().__init__(
            message=f"Task with ID {task_id} not found",
            error_code="TASK_NOT_FOUND",
            details={"task_id": task_id}
        )

class ValidationError(TodoError):
    """Raised when task data validation fails."""
    def __init__(self, message: str, field: str):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            details={"field": field}
        )

class StorageError(TodoError):
    """Raised when there are issues with task storage operations."""
    def __init__(self, operation: str, details: Dict[str, Any]):
        super().__init__(
            message=f"Storage operation '{operation}' failed",
            error_code="STORAGE_ERROR",
            details=details
        )

class ErrorHandler:
    @staticmethod
    def format_error_response(error: TodoError) -> Dict[str, Any]:
        """Format error response for API endpoints."""
        return {
            "error": {
                "code": error.error_code,
                "message": error.message,
                "details": error.details
            }
        }

    @staticmethod
    def handle_validation(title: str, description: str = "") -> None:
        """Validate task data and raise appropriate errors."""
        if not title or not title.strip():
            raise ValidationError("Title cannot be empty", "title")
        if len(title) > 200:
            raise ValidationError("Title is too long (max 200 characters)", "title")
        if len(description) > 1000:
            raise ValidationError("Description is too long (max 1000 characters)", "description")