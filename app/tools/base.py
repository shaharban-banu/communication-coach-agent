"""
Base abstraction for communication tools.

This module defines the common interface that all communication
tools must implement.
"""

from abc import ABC, abstractmethod
from typing import Any

from app.agents.tool_plan import CommunicationTool


class BaseCommunicationTool(ABC):
    """
    Abstract base class for all communication tools.

    Each concrete communication tool must provide its tool type
    and implement the execute method.
    """

    @property
    @abstractmethod
    def tool_type(self) -> CommunicationTool:
        """
        Return the type of communication tool.

        Returns:
            CommunicationTool: Tool identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def execute(self,message: str,context: str | None = None,) -> dict[str, Any]:
        """
        Execute the communication tool.

        Args:
            message: User's communication content.
            context: Optional contextual information.

        Returns:
            dict[str, Any]: Tool execution result.
        """
        raise NotImplementedError