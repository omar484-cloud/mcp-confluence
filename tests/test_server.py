"""
Tests for MCP Server
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from src.server import MCPConfluenceServer
from src.config import Settings


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
def server(mock_settings):
    """Create server instance"""
    with patch('src.client.requests.Session'):
        return MCPConfluenceServer(mock_settings)


def test_server_initialization(server):
    """Test server initialization"""
    assert server.settings is not None
    assert server.client is not None
    assert len(server.tools) > 0


def test_list_tools(server):
    """Test listing available tools"""
    tools = server.list_tools()
    assert isinstance(tools, list)
    assert len(tools) > 0

    tool_names = {tool['name'] for tool in tools}
    expected_tools = {
        'search_pages',
        'search_spaces',
        'get_page',
        'create_page',
        'update_page',
        'delete_page',
        'get_space',
        'list_spaces',
        'get_space_pages',
        'get_page_history',
        'get_page_attachments',
        'get_page_comments',
    }
    assert expected_tools.issubset(tool_names)


def test_get_server_info(server):
    """Test getting server information"""
    info = server.get_server_info()
    assert 'name' in info
    assert 'version' in info
    assert 'deployment' in info
    assert info['deployment'] == 'cloud'


@pytest.mark.asyncio
async def test_call_unknown_tool(server):
    """Test calling unknown tool"""
    result = await server.call_tool('unknown_tool')
    assert not result['success']
    assert 'error' in result


@pytest.mark.asyncio
async def test_call_valid_tool(server):
    """Test calling valid tool"""
    with patch.object(server.client, 'list_spaces', return_value={'results': []}):
        result = await server.call_tool('list_spaces')
        assert result['success']
        assert result['tool'] == 'list_spaces'


@pytest.mark.asyncio
async def test_handle_list_tools_request(server):
    """Test handling list_tools request"""
    request = {
        'request_id': '1',
        'method': 'list_tools',
        'params': {}
    }
    response = await server.handle_request(request)

    assert response['success']
    assert response['request_id'] == '1'
    assert 'data' in response


@pytest.mark.asyncio
async def test_handle_get_server_info_request(server):
    """Test handling get_server_info request"""
    request = {
        'request_id': '2',
        'method': 'get_server_info',
        'params': {}
    }
    response = await server.handle_request(request)

    assert response['success']
    assert 'data' in response


@pytest.mark.asyncio
async def test_handle_call_tool_request(server):
    """Test handling call_tool request"""
    with patch.object(server.client, 'list_spaces', return_value={'results': []}):
        request = {
            'request_id': '3',
            'method': 'call_tool',
            'params': {
                'name': 'list_spaces',
                'arguments': {}
            }
        }
        response = await server.handle_request(request)

        assert response['success']
        assert 'data' in response


@pytest.mark.asyncio
async def test_handle_invalid_method(server):
    """Test handling invalid method"""
    request = {
        'request_id': '4',
        'method': 'invalid_method',
        'params': {}
    }
    response = await server.handle_request(request)

    assert not response['success']
    assert 'error' in response

