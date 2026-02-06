class BaseAPIException(Exception):
    """Base class for all API exceptions"""
    pass

class DatabaseException(BaseAPIException):
    """Raised when a database operation fails"""
    pass

class DuplicateException(DatabaseException):
    """Raised when a unique constraint is violated (e.g. duplicate username)"""
    pass

class NotFoundException(DatabaseException):
    """Raised when a resource is not found"""
    pass

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

class CoreApiException(Exception): ...


class DatabaseException(CoreApiException): ...


class DuplicateException(CoreApiException): ...


class NotFoundException(CoreApiException): ...
