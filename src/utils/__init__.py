"""
Utils package initialization
"""

from src.utils.logger import setup_logging, LoggerMixin
from src.utils.errors import (
    ConfluenceError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    BadRequestError,
    RateLimitError,
    ConfluenceServerError,
)

__all__ = [
    # Logger
    'setup_logging',
    'LoggerMixin',
    # Errors
    'ConfluenceError',
    'AuthenticationError',
    'AuthorizationError',
    'NotFoundError',
    'BadRequestError',
    'RateLimitError',
    'ConfluenceServerError',
]

