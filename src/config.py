"""
Configuration management for MCP Confluence Server
"""

from typing import Optional, Literal
from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    model_config = ConfigDict(env_file='.env', extra='ignore')

    # Confluence Configuration
    confluence_url: str = Field(
        ...,
        description="Base URL of Confluence instance"
    )
    confluence_username: str = Field(
        ...,
        description="Username for Confluence authentication"
    )
    confluence_api_token: str = Field(
        ...,
        description="API token for Confluence authentication"
    )
    confluence_deployment: Literal["cloud", "server"] = Field(
        default="cloud",
        description="Confluence deployment type (cloud or server)"
    )

    # Logging Configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )

    # Request Configuration
    request_timeout: int = Field(
        default=30,
        description="Timeout for HTTP requests in seconds"
    )
    max_retries: int = Field(
        default=3,
        description="Maximum number of retries for failed requests"
    )
    rate_limit_delay: float = Field(
        default=1.0,
        description="Delay in seconds before retrying after rate limit"
    )

    # Proxy Configuration (Optional)
    http_proxy: Optional[str] = Field(
        default=None,
        description="HTTP proxy URL"
    )
    https_proxy: Optional[str] = Field(
        default=None,
        description="HTTPS proxy URL"
    )

    @property
    def proxies(self) -> Optional[dict]:
        """Get proxy configuration"""
        if self.http_proxy or self.https_proxy:
            return {
                "http": self.http_proxy,
                "https": self.https_proxy,
            }
        return None

    def get_auth_tuple(self) -> tuple[str, str]:
        """Get authentication tuple for requests"""
        return (self.confluence_username, self.confluence_api_token)


def get_settings() -> Settings:
    """Get application settings, loading from .env if available"""
    return Settings()

