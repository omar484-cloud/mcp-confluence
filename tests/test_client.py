"""
Tests for Confluence API Client
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.client import ConfluenceClient
from src.config import Settings
from src.utils.errors import (
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    BadRequestError,
)


@pytest.fixture
def mock_settings():
    """Create mock settings"""
    return Settings(
        confluence_url="https://test.atlassian.net",
        confluence_username="test@example.com",
        confluence_api_token="test-token",
        confluence_deployment="cloud",
    )


@pytest.fixture
def client(mock_settings):
    """Create client with mocked session"""
    with patch('src.client.requests.Session'):
        return ConfluenceClient(mock_settings)


def test_client_initialization(mock_settings):
    """Test client initialization"""
    with patch('src.client.requests.Session'):
        client = ConfluenceClient(mock_settings)
        assert client.base_url == "https://test.atlassian.net"
        assert client.deployment == "cloud"


def test_build_url_cloud(client):
    """Test URL building for cloud deployment"""
    url = client._build_url('/content')
    assert "rest/api/3/content" in url


def test_search_pages(client, sample_search_results):
    """Test search pages"""
    with patch.object(client, '_request_with_retry', return_value=sample_search_results):
        results = client.search_pages('title~"test"', limit=25)
        assert len(results['results']) == 1
        assert results['results'][0]['title'] == 'Test Page'


def test_get_page(client, sample_page):
    """Test get page by ID"""
    with patch.object(client, '_request_with_retry', return_value=sample_page):
        page = client.get_page('12345')
        assert page['id'] == '12345'
        assert page['title'] == 'Sample Page'


def test_create_page(client, sample_page):
    """Test create page"""
    with patch.object(client, '_request_with_retry', return_value=sample_page):
        page = client.create_page(
            space_key='DEV',
            title='Sample Page',
            body='<p>Sample content</p>'
        )
        assert page['id'] == '12345'
        assert page['title'] == 'Sample Page'


def test_update_page(client, sample_page):
    """Test update page"""
    with patch.object(client, '_request_with_retry', return_value=sample_page):
        page = client.update_page(
            page_id='12345',
            title='Updated Page',
            body='<p>Updated content</p>',
            version_number=1
        )
        assert page['id'] == '12345'


def test_delete_page(client):
    """Test delete page"""
    with patch.object(client, '_request_with_retry', return_value={}):
        client.delete_page('12345')


def test_get_space(client, sample_space):
    """Test get space"""
    with patch.object(client, '_request_with_retry', return_value=sample_space):
        space = client.get_space('DEV')
        assert space['key'] == 'DEV'
        assert space['name'] == 'Development'


def test_list_spaces(client):
    """Test list spaces"""
    spaces_result = {
        'results': [
            {'key': 'DEV', 'name': 'Development'},
            {'key': 'PROD', 'name': 'Production'},
        ],
        'size': 2,
        'start': 0,
        'limit': 25,
    }
    with patch.object(client, '_request_with_retry', return_value=spaces_result):
        result = client.list_spaces()
        assert len(result['results']) == 2


def test_handle_response_401(client):
    """Test handling 401 Unauthorized response"""
    mock_response = Mock()
    mock_response.status_code = 401

    with pytest.raises(AuthenticationError):
        client._handle_response(mock_response)


def test_handle_response_403(client):
    """Test handling 403 Forbidden response"""
    mock_response = Mock()
    mock_response.status_code = 403

    with pytest.raises(AuthorizationError):
        client._handle_response(mock_response)


def test_handle_response_404(client):
    """Test handling 404 Not Found response"""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.url = "https://test.atlassian.net/rest/api/3/content/999"

    with pytest.raises(NotFoundError):
        client._handle_response(mock_response)


def test_handle_response_400(client):
    """Test handling 400 Bad Request response"""
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {'message': 'Invalid parameter'}

    with pytest.raises(BadRequestError):
        client._handle_response(mock_response)


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


@pytest.fixture
def sample_page():
    """Sample page data"""
    return {
        'id': '12345',
        'type': 'page',
        'title': 'Sample Page',
        'status': 'current',
        'space': {'key': 'DEV'},
    }


@pytest.fixture
def sample_space():
    """Sample space data"""
    return {
        'id': '123',
        'key': 'DEV',
        'name': 'Development',
        'type': 'global',
    }

