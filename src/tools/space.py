"""
Space tools for Confluence
"""

from typing import Dict, Any, List
from src.tools.base import BaseTool, ToolParameter


class GetSpaceTool(BaseTool):
    """Get space information"""

    @property
    def name(self) -> str:
        return "get_space"

    @property
    def description(self) -> str:
        return "Get information about a specific Confluence space"

    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="space_key",
                type="string",
                description="The key of the space to retrieve",
                required=True
            ),
        ]

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute get space"""
        self.validate_parameters(**kwargs)

        space_key = kwargs['space_key']
        space = self.client.get_space(space_key)

        return {
            'success': True,
            'space': space,
        }


class ListSpacesTool(BaseTool):
    """List all spaces"""

    @property
    def name(self) -> str:
        return "list_spaces"

    @property
    def description(self) -> str:
        return "List all available Confluence spaces"

    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="limit",
                type="integer",
                description="Maximum number of spaces to return",
                required=False
            ),
            ToolParameter(
                name="start",
                type="integer",
                description="Starting index for pagination",
                required=False
            ),
        ]

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute list spaces"""
        self.validate_parameters(**kwargs)

        limit = kwargs.get('limit', 25)
        start = kwargs.get('start', 0)

        results = self.client.list_spaces(limit=limit, start=start)

        return {
            'success': True,
            'spaces': results.get('results', []),
            'total': results.get('size', 0),
            'start': results.get('start', 0),
            'limit': results.get('limit', 0),
        }


class GetSpacePagesTool(BaseTool):
    """Get pages in a space"""

    @property
    def name(self) -> str:
        return "get_space_pages"

    @property
    def description(self) -> str:
        return "List all pages in a specific space"

    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="space_key",
                type="string",
                description="The key of the space",
                required=True
            ),
            ToolParameter(
                name="limit",
                type="integer",
                description="Maximum number of pages to return",
                required=False
            ),
            ToolParameter(
                name="start",
                type="integer",
                description="Starting index for pagination",
                required=False
            ),
        ]

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute get space pages"""
        self.validate_parameters(**kwargs)

        space_key = kwargs['space_key']
        limit = kwargs.get('limit', 25)
        start = kwargs.get('start', 0)

        results = self.client.get_space_pages(
            space_key=space_key,
            limit=limit,
            start=start
        )

        return {
            'success': True,
            'pages': results.get('results', []),
            'total': results.get('size', 0),
            'start': results.get('start', 0),
            'limit': results.get('limit', 0),
        }

