from typing import Any, Optional


class CoreApiException(Exception):
    def __init__(
        self, message: str, debug_info: Optional[Any] = None, status_code: int = 500
    ):
        self.message = message
        self.debug_info = debug_info
        self.status_code = status_code
        super().__init__(self.message)


class DatabaseException(CoreApiException):
    def __init__(self, message: str, debug_info: Any = None):
        super().__init__(message, debug_info, status_code=500)


class DuplicateException(CoreApiException):
    def __init__(self, message: str = "Document already exists"):
        super().__init__(message)


class NotFoundException(CoreApiException):
    def __init__(self, message: str, debug_info: Any = None):
        super().__init__(message, debug_info, status_code=404)
