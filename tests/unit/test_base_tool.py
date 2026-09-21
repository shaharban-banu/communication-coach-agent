"""
Tests for the base communication tool abstraction.
"""

from typing import Any

import pytest

from app.agents.tool_plan import CommunicationTool
from app.tools.base import BaseCommunicationTool


class TestTool(BaseCommunicationTool):
    """
    Concrete test implementation of the base tool.
    """

    @property
    def tool_type(self) -> CommunicationTool:
        """
        Return the test tool type.

        Returns:
            CommunicationTool: Grammar correction tool type.
        """
        return CommunicationTool.GRAMMAR_CORRECTION

    def execute(
        self,
        message: str,
        context: str | None = None,
    ) -> dict[str, Any]:
        """
        Execute the test tool.

        Args:
            message: Input message.
            context: Optional context.

        Returns:
            dict[str, Any]: Test result.
        """
        return {
            "message": message,
            "context": context,
        }


def test_base_tool_contract() -> None:
    """
    Verify that a concrete tool follows the base contract.
    """
    tool = TestTool()

    assert tool.tool_type == CommunicationTool.GRAMMAR_CORRECTION

    result = tool.execute(
        message="Test message",
        context="Test context",
    )

    assert result["message"] == "Test message"
    assert result["context"] == "Test context"


def test_base_tool_cannot_be_instantiated() -> None:
    """
    Verify that the abstract base tool cannot be instantiated directly.
    """
    with pytest.raises(TypeError):
        BaseCommunicationTool()