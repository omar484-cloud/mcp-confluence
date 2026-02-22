"""
Confluence API Client
"""

import logging
import time
from typing import Optional, Dict, Any, List
from requests.auth import HTTPBasicAuth
import requests
from urllib.parse import urljoin

from src.config import Settings
from src.utils.errors import (
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    BadRequestError,
    RateLimitError,
    ConfluenceServerError,
)


class ConfluenceClient:
    """
    Client for interacting with Confluence REST API
    Supports both Cloud and Server deployments
    """

    def __init__(self, settings: Settings):
        """
        Initialize Confluence client

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.base_url = settings.confluence_url.rstrip('/')
        self.deployment = settings.confluence_deployment
        self.session = self._create_session()
        self.logger = logging.getLogger(__name__)

    def _create_session(self) -> requests.Session:
        """Create and configure HTTP session"""
        session = requests.Session()
        session.auth = HTTPBasicAuth(
            self.settings.confluence_username,
            self.settings.confluence_api_token
        )
        session.headers.update({
            'User-Agent': 'MCP-Confluence/1.0',
            'Content-Type': 'application/json',
        })

        if self.settings.proxies:
            session.proxies.update(self.settings.proxies)

        return session

    def _build_url(self, endpoint: str) -> str:
        """Build full API URL"""
        api_path = '/wiki/rest/api' if self.deployment == 'server' else '/rest/api/3'
        return urljoin(self.base_url, f"{api_path}{endpoint}")

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API response and raise appropriate exceptions

        Args:
            response: Response object from requests

        Returns:
            Parsed JSON response

        Raises:
            Various ConfluenceError subclasses
        """
        # Handle different status codes
        if response.status_code == 401:
            raise AuthenticationError("Invalid credentials")
        elif response.status_code == 403:
            raise AuthorizationError("Insufficient permissions")
        elif response.status_code == 404:
            raise NotFoundError(f"Resource not found: {response.url}")
        elif response.status_code == 400:
            error_msg = response.json().get('message', 'Bad request')
            raise BadRequestError(error_msg)
        elif response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            raise RateLimitError(retry_after=retry_after)
        elif response.status_code >= 500:
            raise ConfluenceServerError(f"Server error: {response.text}")

        response.raise_for_status()

        # Return JSON if available, otherwise empty dict
        if response.text:
            return response.json()
        return {}

    def _request_with_retry(
        self,
        method: str,
        endpoint: str,
        max_retries: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make HTTP request with retry logic for rate limits

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            max_retries: Maximum number of retries
            **kwargs: Additional arguments to pass to requests

        Returns:
            Response JSON
        """
        max_retries = max_retries or self.settings.max_retries
        url = self._build_url(endpoint)

        for attempt in range(max_retries + 1):
            try:
                self.logger.debug(f"{method} {endpoint}")
                response = self.session.request(method, url, timeout=self.settings.request_timeout, **kwargs)
                return self._handle_response(response)
            except RateLimitError as e:
                if attempt < max_retries:
                    wait_time = e.retry_after + (attempt * self.settings.rate_limit_delay)
                    self.logger.warning(f"Rate limited. Waiting {wait_time}s before retry")
                    time.sleep(wait_time)
                else:
                    raise

    def search_pages(
        self,
        cql: str,
        limit: int = 25,
        start: int = 0,
        expand: str = "space,history.lastUpdated,body.storage"
    ) -> Dict[str, Any]:
        """
        Search for pages using CQL query

        Args:
            cql: CQL query string
            limit: Results limit (max 100)
            start: Pagination start
            expand: Fields to expand

        Returns:
            Search results
        """
        params = {
            'cql': cql,
            'limit': min(limit, 100),
            'start': start,
            'expand': expand,
        }
        return self._request_with_retry('GET', '/content/search', params=params)

    def get_page(self, page_id: str, expand: str = "space,body.storage,history.lastUpdated") -> Dict[str, Any]:
        """
        Get a page by ID

        Args:
            page_id: Page ID
            expand: Fields to expand

        Returns:
            Page data
        """
        params = {'expand': expand}
        return self._request_with_retry('GET', f'/content/{page_id}', params=params)

    def get_page_by_title(self, title: str, space_key: str, expand: str = "space,body.storage") -> Optional[Dict[str, Any]]:
        """
        Get a page by title and space key

        Args:
            title: Page title
            space_key: Space key
            expand: Fields to expand

        Returns:
            Page data or None if not found
        """
        cql = f'title="{title}" AND space.key="{space_key}"'
        results = self.search_pages(cql, limit=1, expand=expand)

        if results.get('results'):
            return results['results'][0]
        return None

    def create_page(
        self,
        space_key: str,
        title: str,
        body: str,
        parent_id: Optional[str] = None,
        representation: str = "storage"
    ) -> Dict[str, Any]:
        """
        Create a new page

        Args:
            space_key: Space key
            title: Page title
            body: Page body content
            parent_id: Parent page ID (for child pages)
            representation: Content representation ('storage' or 'view')

        Returns:
            Created page data
        """
        payload = {
            'type': 'page',
            'title': title,
            'space': {'key': space_key},
            'body': {
                representation: {'value': body}
            }
        }

        if parent_id:
            payload['ancestors'] = [{'id': parent_id}]

        return self._request_with_retry('POST', '/content', json=payload)

    def update_page(
        self,
        page_id: str,
        title: str,
        body: str,
        version_number: Optional[int] = None,
        representation: str = "storage"
    ) -> Dict[str, Any]:
        """
        Update a page

        Args:
            page_id: Page ID
            title: New page title
            body: New page body
            version_number: Current version number (will be incremented)
            representation: Content representation

        Returns:
            Updated page data
        """
        # Get current version if not provided
        if version_number is None:
            page = self.get_page(page_id)
            version_number = page.get('version', {}).get('number', 0)

        payload = {
            'type': 'page',
            'title': title,
            'body': {
                representation: {'value': body}
            },
            'version': {
                'number': version_number + 1
            }
        }

        return self._request_with_retry('PUT', f'/content/{page_id}', json=payload)

    def delete_page(self, page_id: str) -> None:
        """
        Delete a page

        Args:
            page_id: Page ID
        """
        self._request_with_retry('DELETE', f'/content/{page_id}')

    def get_space(self, space_key: str, expand: str = "metadata.labels") -> Dict[str, Any]:
        """
        Get space information

        Args:
            space_key: Space key
            expand: Fields to expand

        Returns:
            Space data
        """
        params = {'expand': expand}
        return self._request_with_retry('GET', f'/spaces/{space_key}', params=params)

    def list_spaces(self, limit: int = 25, start: int = 0) -> Dict[str, Any]:
        """
        List all spaces

        Args:
            limit: Results limit
            start: Pagination start

        Returns:
            Spaces list
        """
        params = {
            'limit': min(limit, 100),
            'start': start,
        }
        return self._request_with_retry('GET', '/spaces', params=params)

    def get_space_pages(self, space_key: str, limit: int = 25, start: int = 0) -> Dict[str, Any]:
        """
        Get pages in a space

        Args:
            space_key: Space key
            limit: Results limit
            start: Pagination start

        Returns:
            Pages list
        """
        cql = f'space.key="{space_key}" AND type=page'
        return self.search_pages(cql, limit=limit, start=start)

    def get_page_history(self, page_id: str, limit: int = 10) -> Dict[str, Any]:
        """
        Get page revision history

        Args:
            page_id: Page ID
            limit: Number of versions to return

        Returns:
            Version history
        """
        params = {
            'expand': 'history.byUser',
            'limit': min(limit, 20),
        }
        return self._request_with_retry('GET', f'/content/{page_id}/history', params=params)

    def get_page_attachments(self, page_id: str, limit: int = 10) -> Dict[str, Any]:
        """
        Get page attachments

        Args:
            page_id: Page ID
            limit: Number of attachments to return

        Returns:
            Attachments list
        """
        params = {'limit': min(limit, 50)}
        return self._request_with_retry('GET', f'/content/{page_id}/child/attachment', params=params)

    def get_page_comments(self, page_id: str, limit: int = 10) -> Dict[str, Any]:
        """
        Get page comments

        Args:
            page_id: Page ID
            limit: Number of comments to return

        Returns:
            Comments list
        """
        params = {'limit': min(limit, 50)}
        return self._request_with_retry('GET', f'/content/{page_id}/child/comment', params=params)

