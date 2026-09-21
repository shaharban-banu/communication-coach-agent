"""
Tests for the communication tool registry.
"""

from typing import Any

import pytest

from app.agents.tool_plan import CommunicationTool
from app.core.exceptions import ToolExecutionException
from app.tools.base import BaseCommunicationTool
from app.tools.registry import ToolRegistry


class TestTool(BaseCommunicationTool):
    """Test implementation of a communication tool."""

    @property
    def tool_type(self) -> CommunicationTool:
        """Return the test tool identifier."""
        return CommunicationTool.GRAMMAR_CORRECTION

    def execute(
        self,
        message: str,
        context: str | None = None,
    ) -> dict[str, Any]:
        """Return a test result."""
        return {"message": message}


def test_register_and_get_tool() -> None:
    """
    Verify that a registered tool can be retrieved.
    """
    registry = ToolRegistry()
    tool = TestTool()

    registry.register(tool)

    assert registry.get(
        CommunicationTool.GRAMMAR_CORRECTION
    ) is tool


def test_duplicate_tool_registration_fails() -> None:
    """
    Verify that duplicate tool registration is rejected.
    """
    registry = ToolRegistry()

    registry.register(TestTool())

    with pytest.raises(ToolExecutionException):
        registry.register(TestTool())


def test_missing_tool_fails() -> None:
    """
    Verify that an unregistered tool raises an exception.
    """
    registry = ToolRegistry()

    with pytest.raises(ToolExecutionException):
        registry.get(
            CommunicationTool.EMAIL_GENERATION
        )