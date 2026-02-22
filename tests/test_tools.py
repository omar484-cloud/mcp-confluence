"""
Tests for MCP Tools
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.tools.search import SearchPagesTool, SearchSpacesTool
from src.tools.page import GetPageTool, CreatePageTool, UpdatePageTool, DeletePageTool
from src.tools.space import GetSpaceTool, ListSpacesTool, GetSpacePagesTool
from src.tools.metadata import GetPageHistoryTool, GetPageAttachmentsTool, GetPageCommentsTool


@pytest.fixture
def mock_client():
    """Create mock client"""
    return Mock()


class TestSearchPagesTool:

    async def test_search_pages_tool(self, mock_client):
        """Test search pages tool"""
        tool = SearchPagesTool(mock_client)
        assert tool.name == 'search_pages'
        assert len(tool.parameters) > 0

    @pytest.mark.asyncio
    async def test_search_pages_execute(self, mock_client):
        """Test execute search pages"""
        mock_client.search_pages.return_value = {
            'results': [{'id': '1', 'title': 'Test'}],
            'size': 1,
            'start': 0,
            'limit': 25,
        }

        tool = SearchPagesTool(mock_client)
        result = await tool.execute(query='title~"test"', limit=25)

        assert result['success']
        assert len(result['results']) == 1

    def test_search_pages_validate_required_params(self, mock_client):
        """Test parameter validation"""
        tool = SearchPagesTool(mock_client)

        with pytest.raises(ValueError):
            tool.validate_parameters(limit=25)  # Missing required 'query'


class TestPageTools:

    @pytest.mark.asyncio
    async def test_get_page_execute(self, mock_client):
        """Test get page tool"""
        mock_client.get_page.return_value = {
            'id': '123',
            'title': 'Test Page'
        }

        tool = GetPageTool(mock_client)
        result = await tool.execute(page_id='123')

        assert result['success']
        assert result['page']['id'] == '123'

    @pytest.mark.asyncio
    async def test_create_page_execute(self, mock_client):
        """Test create page tool"""
        mock_client.create_page.return_value = {
            'id': '456',
            'title': 'New Page'
        }

        tool = CreatePageTool(mock_client)
        result = await tool.execute(
            space_key='DEV',
            title='New Page',
            body='<p>Content</p>'
        )

        assert result['success']
        assert result['page_id'] == '456'

    @pytest.mark.asyncio
    async def test_update_page_execute(self, mock_client):
        """Test update page tool"""
        mock_client.update_page.return_value = {
            'id': '123',
            'title': 'Updated Page'
        }

        tool = UpdatePageTool(mock_client)
        result = await tool.execute(
            page_id='123',
            title='Updated Page',
            body='<p>Updated</p>'
        )

        assert result['success']

    @pytest.mark.asyncio
    async def test_delete_page_execute(self, mock_client):
        """Test delete page tool"""
        mock_client.delete_page.return_value = None

        tool = DeletePageTool(mock_client)
        result = await tool.execute(page_id='123')

        assert result['success']


class TestSpaceTools:

    @pytest.mark.asyncio
    async def test_get_space_execute(self, mock_client):
        """Test get space tool"""
        mock_client.get_space.return_value = {
            'key': 'DEV',
            'name': 'Development'
        }

        tool = GetSpaceTool(mock_client)
        result = await tool.execute(space_key='DEV')

        assert result['success']
        assert result['space']['key'] == 'DEV'

    @pytest.mark.asyncio
    async def test_list_spaces_execute(self, mock_client):
        """Test list spaces tool"""
        mock_client.list_spaces.return_value = {
            'results': [
                {'key': 'DEV', 'name': 'Development'}
            ],
            'size': 1,
            'start': 0,
            'limit': 25,
        }

        tool = ListSpacesTool(mock_client)
        result = await tool.execute()

        assert result['success']
        assert len(result['spaces']) == 1

    @pytest.mark.asyncio
    async def test_get_space_pages_execute(self, mock_client):
        """Test get space pages tool"""
        mock_client.get_space_pages.return_value = {
            'results': [
                {'id': '1', 'title': 'Page 1'}
            ],
            'size': 1,
            'start': 0,
            'limit': 25,
        }

        tool = GetSpacePagesTool(mock_client)
        result = await tool.execute(space_key='DEV')

        assert result['success']
        assert len(result['pages']) == 1


class TestMetadataTools:

    @pytest.mark.asyncio
    async def test_get_page_history_execute(self, mock_client):
        """Test get page history tool"""
        mock_client.get_page_history.return_value = {
            'results': [
                {'number': 1, 'by': {'displayName': 'User'}}
            ],
            'size': 1,
        }

        tool = GetPageHistoryTool(mock_client)
        result = await tool.execute(page_id='123')

        assert result['success']
        assert len(result['versions']) == 1

    @pytest.mark.asyncio
    async def test_get_page_attachments_execute(self, mock_client):
        """Test get page attachments tool"""
        mock_client.get_page_attachments.return_value = {
            'results': [
                {'id': '1', 'title': 'file.pdf'}
            ],
            'size': 1,
        }

        tool = GetPageAttachmentsTool(mock_client)
        result = await tool.execute(page_id='123')

        assert result['success']
        assert len(result['attachments']) == 1

    @pytest.mark.asyncio
    async def test_get_page_comments_execute(self, mock_client):
        """Test get page comments tool"""
        mock_client.get_page_comments.return_value = {
            'results': [
                {'id': '1', 'body': 'Nice page!'}
            ],
            'size': 1,
        }

        tool = GetPageCommentsTool(mock_client)
        result = await tool.execute(page_id='123')

        assert result['success']
        assert len(result['comments']) == 1


def test_tool_to_dict(mock_client):
    """Test tool definition serialization"""
    tool = GetPageTool(mock_client)
    tool_dict = tool.to_dict()

    assert 'name' in tool_dict
    assert 'description' in tool_dict
    assert 'parameters' in tool_dict
    assert isinstance(tool_dict['parameters'], list)

