"""
MCP Server implementation for Confluence
"""

import logging
from typing import Dict, Any, List, Optional
import asyncio

from src.client import ConfluenceClient
from src.config import Settings
from src.tools import (
    SearchPagesTool,
    SearchSpacesTool,
    GetPageTool,
    CreatePageTool,
    UpdatePageTool,
    DeletePageTool,
    GetSpaceTool,
    ListSpacesTool,
    GetSpacePagesTool,
    GetPageHistoryTool,
    GetPageAttachmentsTool,
    GetPageCommentsTool,
)


class MCPConfluenceServer:
    """
    MCP Server for Confluence integration
    Implements the Model Context Protocol for LLM interaction with Confluence
    """

    def __init__(self, settings: Settings):
        """
        Initialize MCP server

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.logger = logging.getLogger(__name__)

        # Initialize Confluence client
        self.client = ConfluenceClient(settings)

        # Initialize tools
        self.tools = self._initialize_tools()

    def _initialize_tools(self) -> Dict[str, Any]:
        """Initialize all available tools"""
        tools = {
            # Search tools
            SearchPagesTool(self.client),
            SearchSpacesTool(self.client),
            # Page tools
            GetPageTool(self.client),
            CreatePageTool(self.client),
            UpdatePageTool(self.client),
            DeletePageTool(self.client),
            # Space tools
            GetSpaceTool(self.client),
            ListSpacesTool(self.client),
            GetSpacePagesTool(self.client),
            # Metadata tools
            GetPageHistoryTool(self.client),
            GetPageAttachmentsTool(self.client),
            GetPageCommentsTool(self.client),
        }

        # Build tool registry by name
        return {tool.name: tool for tool in tools}

    def list_tools(self) -> List[Dict[str, Any]]:
        """
        Get list of available tools

        Returns:
            List of tool definitions
        """
        return [tool.to_dict() for tool in self.tools.values()]

    async def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a tool

        Args:
            tool_name: Name of the tool to execute
            **kwargs: Tool parameters

        Returns:
            Tool execution result
        """
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        tool = self.tools[tool_name]
        self.logger.info(f"Calling tool: {tool_name} with params: {kwargs}")

        try:
            result = await tool.execute(**kwargs)
            return {
                'success': True,
                'tool': tool_name,
                'data': result,
            }
        except Exception as e:
            self.logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return {
                'success': False,
                'tool': tool_name,
                'error': str(e),
            }

    def get_server_info(self) -> Dict[str, Any]:
        """Get server information"""
        return {
            'name': 'MCP Confluence Server',
            'version': '1.0.0',
            'description': 'Model Context Protocol server for Atlassian Confluence',
            'deployment': self.settings.confluence_deployment,
            'confluence_url': self.settings.confluence_url,
        }

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle MCP request

        Args:
            request: MCP request object

        Returns:
            MCP response object
        """
        method = request.get('method')
        params = request.get('params', {})
        request_id = request.get('request_id')

        try:
            if method == 'list_tools':
                data = self.list_tools()
            elif method == 'call_tool':
                tool_name = params.get('name')
                tool_params = params.get('arguments', {})
                data = await self.call_tool(tool_name, **tool_params)
            elif method == 'get_server_info':
                data = self.get_server_info()
            else:
                raise ValueError(f"Unknown method: {method}")

            return {
                'request_id': request_id,
                'success': True,
                'data': data,
            }
        except Exception as e:
            self.logger.error(f"Error handling request: {str(e)}")
            return {
                'request_id': request_id,
                'success': False,
                'error': str(e),
            }

