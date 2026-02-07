from typing import Any, Optional


class BaseAPIException(Exception):
    """Base class for all API exceptions"""

    pass


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


class UsernameAlreadyExists(DuplicateException):
    """Raised when the username is already taken during signup"""

    pass


class InvalidCredentials(BaseAPIException):
    """Raised when login fails (wrong password or username)"""

    pass


class InvalidToken(BaseAPIException):
    """Raised when the token is expired, invalid, or malformed"""

    pass


class AuthorizationException(Exception):
    """Raised when authentication fails, tokens are invalid, or permissions are denied."""

    pass
