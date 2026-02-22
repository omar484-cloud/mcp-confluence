"""
Base tool class for MCP Confluence tools
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class ToolParameter(BaseModel):
    """Tool parameter definition"""

    name: str
    type: str = "string"
    description: str
    required: bool = True


class BaseTool(ABC):
    """
    Base class for all MCP tools
    """

    def __init__(self, client):
        """
        Initialize tool with Confluence client

        Args:
            client: ConfluenceClient instance
        """
        self.client = client

    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description"""
        pass

    @property
    @abstractmethod
    def parameters(self) -> List[ToolParameter]:
        """Tool parameters"""
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool

        Args:
            **kwargs: Tool parameters

        Returns:
            Tool result
        """
        pass

    def validate_parameters(self, **kwargs) -> None:
        """
        Validate provided parameters

        Args:
            **kwargs: Parameters to validate

        Raises:
            ValueError: If parameters are invalid
        """
        param_names = {p.name for p in self.parameters}
        provided_keys = set(kwargs.keys())
        required_params = {p.name for p in self.parameters if p.required}

        # Check for missing required parameters
        missing = required_params - provided_keys
        if missing:
            raise ValueError(f"Missing required parameters: {', '.join(missing)}")

        # Check for unexpected parameters
        unexpected = provided_keys - param_names
        if unexpected:
            raise ValueError(f"Unexpected parameters: {', '.join(unexpected)}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert tool definition to dict"""
        return {
            'name': self.name,
            'description': self.description,
            'parameters': [
                {
                    'name': p.name,
                    'type': p.type,
                    'description': p.description,
                    'required': p.required,
                }
                for p in self.parameters
            ]
        }

