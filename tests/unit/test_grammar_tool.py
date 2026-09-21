"""
Unit tests for the grammar correction tool.
"""

from unittest.mock import MagicMock, patch

import pytest

from app.core.exceptions import ToolExecutionException
from app.tools.grammar import GrammarCorrectionTool


@patch("app.tools.grammar.Groq")
def test_grammar_correction_success(mock_groq: MagicMock) -> None:
    """
    Verify successful grammar correction using a mocked Groq response.
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

    tool = GrammarCorrectionTool()

    result = tool.execute(
        "I has completed the task yesterday."
    )

    assert result["corrected_text"] == (
        "I completed the task yesterday."
    )

    assert len(result["changes"]) == 1

    mock_groq.return_value.chat.completions.create.assert_called_once()


@patch("app.tools.grammar.Groq")
def test_grammar_correction_empty_message(
    mock_groq: MagicMock,
) -> None:
    """
    Verify that empty input raises a tool execution exception.
    """
    tool = GrammarCorrectionTool()

    with pytest.raises(ToolExecutionException):
        tool.execute("")

    mock_groq.return_value.chat.completions.create.assert_not_called()


@patch("app.tools.grammar.Groq")
def test_grammar_correction_invalid_json(
    mock_groq: MagicMock,
) -> None:
    """
    Verify that invalid LLM JSON is handled correctly.
    """
    mock_response = MagicMock()

    mock_response.choices[0].message.content = (
        "This is not valid JSON"
    )

    mock_groq.return_value.chat.completions.create.return_value = (
        mock_response
    )

    tool = GrammarCorrectionTool()

    with pytest.raises(ToolExecutionException):
        tool.execute(
            "I has completed the task."
        )