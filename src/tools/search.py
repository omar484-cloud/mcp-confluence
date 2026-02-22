"""
Search tools for Confluence
"""

from typing import Dict, Any, List
from src.tools.base import BaseTool, ToolParameter


class SearchPagesTool(BaseTool):
    """Search for pages using CQL"""

    @property
    def name(self) -> str:
        return "search_pages"

    @property
    def description(self) -> str:
        return "Search for pages in Confluence using CQL (Confluence Query Language)"

    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="query",
                type="string",
                description="CQL query string (e.g., 'title~\"API\" AND space.key=DEV')",
                required=True
            ),
            ToolParameter(
                name="limit",
                type="integer",
                description="Maximum number of results to return (1-100)",
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
        """Execute search"""
        self.validate_parameters(**kwargs)

        query = kwargs['query']
        limit = kwargs.get('limit', 25)
        start = kwargs.get('start', 0)

        results = self.client.search_pages(
            cql=query,
            limit=limit,
            start=start
        )

        return {
            'success': True,
            'results': results.get('results', []),
            'total': results.get('size', 0),
            'start': results.get('start', 0),
            'limit': results.get('limit', 0),
        }


class SearchSpacesTool(BaseTool):
    """Search for spaces"""

    @property
    def name(self) -> str:
        return "search_spaces"

    @property
    def description(self) -> str:
        return "Search for spaces in Confluence"

    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="limit",
                type="integer",
                description="Maximum number of results to return",
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
        """Execute search"""
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

