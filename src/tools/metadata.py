"""
Metadata tools for Confluence
"""

from typing import Dict, Any, List
from src.tools.base import BaseTool, ToolParameter


class GetPageHistoryTool(BaseTool):
    """Get page revision history"""

    @property
    def name(self) -> str:
        return "get_page_history"

    @property
    def description(self) -> str:
        return "Get the revision history of a page"

    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="page_id",
                type="string",
                description="The ID of the page",
                required=True
            ),
            ToolParameter(
                name="limit",
                type="integer",
                description="Maximum number of versions to return",
                required=False
            ),
        ]

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute get page history"""
        self.validate_parameters(**kwargs)

        page_id = kwargs['page_id']
        limit = kwargs.get('limit', 10)

        history = self.client.get_page_history(page_id, limit=limit)

        return {
            'success': True,
            'versions': history.get('results', []),
            'total': history.get('size', 0),
        }


class GetPageAttachmentsTool(BaseTool):
    """Get page attachments"""

    @property
    def name(self) -> str:
        return "get_page_attachments"

    @property
    def description(self) -> str:
        return "Get all attachments on a page"

    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="page_id",
                type="string",
                description="The ID of the page",
                required=True
            ),
            ToolParameter(
                name="limit",
                type="integer",
                description="Maximum number of attachments to return",
                required=False
            ),
        ]

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute get page attachments"""
        self.validate_parameters(**kwargs)

        page_id = kwargs['page_id']
        limit = kwargs.get('limit', 10)

        attachments = self.client.get_page_attachments(page_id, limit=limit)

        return {
            'success': True,
            'attachments': attachments.get('results', []),
            'total': attachments.get('size', 0),
        }


class GetPageCommentsTool(BaseTool):
    """Get page comments"""

    @property
    def name(self) -> str:
        return "get_page_comments"

    @property
    def description(self) -> str:
        return "Get all comments on a page"

    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="page_id",
                type="string",
                description="The ID of the page",
                required=True
            ),
            ToolParameter(
                name="limit",
                type="integer",
                description="Maximum number of comments to return",
                required=False
            ),
        ]

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute get page comments"""
        self.validate_parameters(**kwargs)

        page_id = kwargs['page_id']
        limit = kwargs.get('limit', 10)

        comments = self.client.get_page_comments(page_id, limit=limit)

        return {
            'success': True,
            'comments': comments.get('results', []),
            'total': comments.get('size', 0),
        }

