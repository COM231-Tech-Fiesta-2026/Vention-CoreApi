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