"""
Logging configuration for MCP Confluence Server
"""

import logging
import sys
from typing import Optional


def setup_logging(level: Optional[str] = None) -> logging.Logger:
    """
    Configure logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    log_level = level or "INFO"

    logger = logging.getLogger("mcp_confluence")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Create console handler with formatting
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, log_level.upper()))

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


class LoggerMixin:
    """Mixin class to add logging to any class"""

    @property
    def logger(self) -> logging.Logger:
        """Get logger instance for this class"""
        return logging.getLogger(self.__class__.__module__)

