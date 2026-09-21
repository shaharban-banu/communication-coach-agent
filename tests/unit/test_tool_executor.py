"""
Tests for the communication tool executor.
"""

from typing import Any

from app.agents.intent import CommunicationIntent
from app.agents.tool_plan import (
    CommunicationTool,
    ToolExecutionPlan,
)
from app.tools.base import BaseCommunicationTool
from app.tools.executor import ToolExecutor
from app.tools.registry import ToolRegistry


class TestTool(BaseCommunicationTool):
    """Test implementation used by executor tests."""

    @property
    def tool_type(self) -> CommunicationTool:
        """Return the test tool identifier."""
        return CommunicationTool.GRAMMAR_CORRECTION

    def execute(
        self,
        message: str,
        context: str | None = None,
    ) -> dict[str, Any]:
        """Return a predictable test result."""
        return {
            "corrected_text": message.upper(),
            "context": context,
        }


def test_tool_executor_runs_registered_tool() -> None:
    """
    Verify that the executor resolves and executes a registered tool.
    """
    registry = ToolRegistry()
    registry.register(TestTool())

    executor = ToolExecutor(registry)

    plan = ToolExecutionPlan(
        intent=CommunicationIntent.GRAMMAR_CORRECTION,
        tools=[
            CommunicationTool.GRAMMAR_CORRECTION,
        ],
        reason="Test grammar workflow.",
    )

    results = executor.execute(
        plan=plan,
        message="hello world",
        context="test",
    )

    assert len(results) == 1
    assert results[0]["tool"] == "grammar_correction"
    assert results[0]["result"]["corrected_text"] == "HELLO WORLD"
    assert results[0]["result"]["context"] == "test"