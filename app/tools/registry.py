"""
Registry for communication tools.

This module maps communication tool identifiers to their concrete
tool implementations.
"""
from app.agents.tool_plan import CommunicationTool
from app.core.exceptions import ToolExecutionException
from app.core.logging import get_logger
from app.tools.base import BaseCommunicationTool

logger=get_logger(__name__)

class ToolRegistry:
    """
    Registry containing available communication tools.

    The registry allows the tool executor to resolve a
    CommunicationTool identifier to its concrete implementation.
    """
    def __init__(self):
        self._tools:dict[CommunicationTool,BaseCommunicationTool,]={}
        logger.info("Tool registry initialized")

    def register(self,tool:BaseCommunicationTool,):
        """
        Register a communication tool.

        Args:
            tool: Concrete communication tool implementation.

        Raises:
            ToolExecutionException: If the tool is already registered.
        """
        tool_type=tool.tool_type
        if tool_type in self._tools:
            logger.error(
                "Tool already registered | tool=%s",
                tool_type.value,
            )

            raise ToolExecutionException(
                f"Tool already registered: {tool_type.value}"
            )
        self._tools[tool_type]=tool
        logger.info(
            "Tool registered | tool=%s",
            tool_type.value,
        )

    def get(self,tool_type:CommunicationTool,):
        """
        Retrieve a registered communication tool.

        Args:
            tool_type: Identifier of the requested tool.

        Returns:
            BaseCommunicationTool: Registered tool implementation.

        Raises:
            ToolExecutionException: If the tool is not registered.
        """
        tool = self._tools.get(tool_type)

        if tool is None:
            logger.error(
                "Tool not registered | tool=%s",
                tool_type.value,
            )

            raise ToolExecutionException(
                f"Tool not registered: {tool_type.value}"
            )

        return tool
