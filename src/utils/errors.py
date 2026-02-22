"""
Custom exceptions for MCP Confluence Server
"""


class ConfluenceError(Exception):
    """Base exception for Confluence-related errors"""

    def __init__(self, message: str, error_code: int = 500):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class AuthenticationError(ConfluenceError):
    """Raised when authentication fails"""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 401)


class AuthorizationError(ConfluenceError):
    """Raised when user lacks permissions"""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, 403)


class NotFoundError(ConfluenceError):
    """Raised when a resource is not found"""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)


class BadRequestError(ConfluenceError):
    """Raised when the request is malformed"""

    def __init__(self, message: str = "Bad request"):
        super().__init__(message, 400)


class RateLimitError(ConfluenceError):
    """Raised when rate limited"""

    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = 60):
        super().__init__(message, 429)
        self.retry_after = retry_after


class ConfluenceServerError(ConfluenceError):
    """Raised when Confluence server returns an error"""

    def __init__(self, message: str = "Confluence server error"):
        super().__init__(message, 500)

