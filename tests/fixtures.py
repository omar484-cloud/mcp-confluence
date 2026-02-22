"""
Test fixtures and configuration
"""

import pytest
import json
from unittest.mock import Mock, MagicMock, patch
from src.config import Settings
from src.client import ConfluenceClient
from src.server import MCPConfluenceServer


@pytest.fixture
def mock_settings():
    """Create mock settings"""
    return Settings(
        confluence_url="https://test.atlassian.net",
        confluence_username="test@example.com",
        confluence_api_token="test-token",
        confluence_deployment="cloud",
        log_level="DEBUG",
    )


@pytest.fixture
def mock_client(mock_settings):
    """Create mock Confluence client"""
    with patch('src.client.requests.Session'):
        return ConfluenceClient(mock_settings)


@pytest.fixture
def mcp_server(mock_settings):
    """Create MCP server instance"""
    with patch('src.client.requests.Session'):
        return MCPConfluenceServer(mock_settings)


@pytest.fixture
def sample_page():
    """Sample page data"""
    return {
        'id': '12345',
        'type': 'page',
        'title': 'Sample Page',
        'status': 'current',
        'space': {'key': 'DEV'},
        'body': {
            'storage': {
                'value': '<p>Sample content</p>'
            }
        },
        'version': {
            'number': 1
        },
        '_links': {
            'webui': '/pages/viewpage.action?pageId=12345'
        }
    }


@pytest.fixture
def sample_space():
    """Sample space data"""
    return {
        'id': '123',
        'key': 'DEV',
        'name': 'Development',
        'type': 'global',
        'status': 'current',
    }


@pytest.fixture
def sample_search_results():
    """Sample search results"""
    return {
        'results': [
            {
                'id': '123',
                'type': 'page',
                'title': 'Test Page',
                'space': {'key': 'DEV'},
            }
        ],
        'start': 0,
        'limit': 25,
        'size': 1,
        'totalSize': 1,
    }

