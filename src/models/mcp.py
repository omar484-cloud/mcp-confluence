"""
MCP Protocol models
"""

from typing import Optional, Any, Dict, List
from pydantic import BaseModel, Field


class ToolParameter(BaseModel):
    """MCP tool parameter definition"""

    name: str
    description: str
    required: bool = True
    type: str = "string"  # string, number, boolean, object, array


class ToolDefinition(BaseModel):
    """MCP tool definition"""

    name: str
    description: str
    parameters: List[ToolParameter] = Field(default_factory=list)


class ToolCall(BaseModel):
    """MCP tool call request"""

    name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)


class ToolResult(BaseModel):
    """MCP tool result response"""

    tool_name: str
    success: bool
    result: Any = None
    error: Optional[str] = None
    message: Optional[str] = None


class MCPRequest(BaseModel):
    """MCP server request"""

    request_id: Optional[str] = None
    method: str  # "list_tools", "call_tool", "list_resources", etc.
    params: Dict[str, Any] = Field(default_factory=dict)


class MCPResponse(BaseModel):
    """MCP server response"""

    request_id: Optional[str] = None
    success: bool = True
    data: Optional[Any] = None
    error: Optional[str] = None

