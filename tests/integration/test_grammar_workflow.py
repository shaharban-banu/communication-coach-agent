"""
Integration test for the grammar correction workflow.

The Groq API is mocked so that the complete application tool
pipeline can be tested without making an external API call.
"""

from unittest.mock import MagicMock, patch

from app.agents.intent import CommunicationIntent
from app.agents.planner import CommunicationPlanner
from app.tools.executor import ToolExecutor
from app.tools.factory import create_tool_registry
from app.agents.tool_plan import (
    CommunicationTool,
    ToolExecutionPlan,
)


@patch("app.tools.grammar.Groq")
def test_grammar_correction_end_to_end(
    mock_groq: MagicMock,
) -> None:
    """
    Verify the complete planner-to-tool execution workflow.
    """
    mock_response = MagicMock()

    mock_response.choices[0].message.content = """
    {
        "corrected_text": "I completed the task yesterday.",
        "changes": [
            "Changed 'has completed' to 'completed'."
        ]
    }
    """

    mock_groq.return_value.chat.completions.create.return_value = (
        mock_response
    )

    planner = CommunicationPlanner()

    plan = ToolExecutionPlan(
        intent=CommunicationIntent.GRAMMAR_CORRECTION,
        tools=[
            CommunicationTool.GRAMMAR_CORRECTION,
        ],
        reason="Testing the currently implemented grammar tool.",
    )

    registry = create_tool_registry()

    executor = ToolExecutor(registry)

    results = executor.execute(
        plan=plan,
        message="I has completed the task yesterday.",
    )

    assert len(results) == 1

    assert results[0]["tool"] == "grammar_correction"

    assert results[0]["result"]["corrected_text"] == (
        "I completed the task yesterday."
    )