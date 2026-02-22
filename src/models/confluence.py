"""
Data models for Confluence entities
"""

from typing import Optional, Any, List
from pydantic import BaseModel, Field
from datetime import datetime


class User(BaseModel):
    """Confluence user representation"""

    account_id: str
    display_name: str
    email: Optional[str] = None
    username: Optional[str] = None
    avatar_url: Optional[str] = None


class Version(BaseModel):
    """Page version information"""

    version_number: int
    created_by: User
    created_date: datetime
    message: Optional[str] = None


class Content(BaseModel):
    """Confluence page/content representation"""

    id: str
    type: str  # 'page', 'blogpost', etc.
    title: str
    space_key: str
    status: str = "current"
    body: Optional[str] = None
    version: Optional[Version] = None
    created_by: Optional[User] = None
    created_date: Optional[datetime] = None
    modified_by: Optional[User] = None
    modified_date: Optional[datetime] = None
    url: Optional[str] = None
    parent_id: Optional[str] = None
    labels: List[str] = Field(default_factory=list)
    metadata: Optional[dict] = None


class Space(BaseModel):
    """Confluence space representation"""

    key: str
    name: str
    type: str  # 'global', 'personal'
    status: str = "current"
    description: Optional[str] = None
    homepage_id: Optional[str] = None
    url: Optional[str] = None
    icon: Optional[dict] = None


class SearchResult(BaseModel):
    """Search result representation"""

    title: str
    type: str
    space_key: str
    content_id: str
    url: Optional[str] = None
    excerpt: Optional[str] = None


class PageSearchResults(BaseModel):
    """Search results container"""

    results: List[SearchResult]
    start: int
    limit: int
    size: int
    total_size: int

    @property
    def has_more(self) -> bool:
        """Check if there are more results"""
        return (self.start + self.size) < self.total_size

