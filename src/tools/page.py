"""
Page tools for Confluence
"""

from typing import Dict, Any, List, Optional
from src.tools.base import BaseTool, ToolParameter


class GetPageTool(BaseTool):
    """Get a page by ID"""

    @property
    def name(self) -> str:
        return "get_page"

    @property
    def description(self) -> str:
        return "Retrieve a specific page by its ID"

    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="page_id",
                type="string",
                description="The ID of the page to retrieve",
                required=True
            ),
        ]

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute get page"""
        self.validate_parameters(**kwargs)

        page_id = kwargs['page_id']
        page = self.client.get_page(page_id)

        return {
            'success': True,
            'page': page,
        }


class CreatePageTool(BaseTool):
    """Create a new page"""

    @property
    def name(self) -> str:
        return "create_page"

    @property
    def description(self) -> str:
        return "Create a new page in a Confluence space"

    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="space_key",
                type="string",
                description="The key of the space where the page will be created",
                required=True
            ),
            ToolParameter(
                name="title",
                type="string",
                description="The title of the new page",
                required=True
            ),
            ToolParameter(
                name="body",
                type="string",
                description="The body content of the page (in storage format - Wiki markup or HTML)",
                required=True
            ),
            ToolParameter(
                name="parent_id",
                type="string",
                description="Optional ID of the parent page for creating child pages",
                required=False
            ),
        ]

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute create page"""
        self.validate_parameters(**kwargs)

        space_key = kwargs['space_key']
        title = kwargs['title']
        body = kwargs['body']
        parent_id = kwargs.get('parent_id')

        page = self.client.create_page(
            space_key=space_key,
            title=title,
            body=body,
            parent_id=parent_id
        )

        return {
            'success': True,
            'page_id': page.get('id'),
            'page': page,
        }


class UpdatePageTool(BaseTool):
    """Update a page"""

    @property
    def name(self) -> str:
        return "update_page"

    @property
    def description(self) -> str:
        return "Update the content and title of an existing page"

    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="page_id",
                type="string",
                description="The ID of the page to update",
                required=True
            ),
            ToolParameter(
                name="title",
                type="string",
                description="The new title of the page",
                required=True
            ),
            ToolParameter(
                name="body",
                type="string",
                description="The new body content of the page",
                required=True
            ),
            ToolParameter(
                name="version_number",
                type="integer",
                description="Current version number (optional, will be fetched if not provided)",
                required=False
            ),
        ]

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute update page"""
        self.validate_parameters(**kwargs)

        page_id = kwargs['page_id']
        title = kwargs['title']
        body = kwargs['body']
        version_number = kwargs.get('version_number')

        page = self.client.update_page(
            page_id=page_id,
            title=title,
            body=body,
            version_number=version_number
        )

        return {
            'success': True,
            'page': page,
        }


class DeletePageTool(BaseTool):
    """Delete a page"""

    @property
    def name(self) -> str:
        return "delete_page"

    @property
    def description(self) -> str:
        return "Delete a page from Confluence"

    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="page_id",
                type="string",
                description="The ID of the page to delete",
                required=True
            ),
        ]

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute delete page"""
        self.validate_parameters(**kwargs)

        page_id = kwargs['page_id']
        self.client.delete_page(page_id)

        return {
            'success': True,
            'message': f'Page {page_id} deleted successfully',
        }

