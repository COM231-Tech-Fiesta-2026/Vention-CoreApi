from typing import Any, Optional


class CoreApiException(Exception):
    def __init__(
        self,
        message: str = "An internal error occured.",
        debug_info: Optional[Any] = None,
        status_code: int = 500,
    ):
        self.message = message
        self.debug_info = debug_info
        self.status_code = status_code
        super().__init__(self.message)


class DatabaseException(CoreApiException):
    def __init__(
        self, message: str = "A database error occured.", debug_info: Any = None
    ):
        super().__init__(message, debug_info, status_code=500)


class DuplicateException(CoreApiException):
    def __init__(self, message: str = "Document already exists"):
        super().__init__(message)


class NotFoundException(CoreApiException):
    def __init__(self, message: str = "Resource not found.", debug_info: Any = None):
        super().__init__(message, debug_info, status_code=404)


class UserNotFoundException(CoreApiException):
    def __init__(
        self,
        message: str = "User not found.",
        debug_info: Any | None = None,
        status_code: int = 400,
    ):
        super().__init__(message, debug_info, status_code)


class ConversationNotFoundException(CoreApiException):
    def __init__(
        self,
        message: str = "The requested conversation could not be found.",
        debug_info: Any | None = None,
        status_code: int = 404,
    ):
        super().__init__(message, debug_info, status_code)
