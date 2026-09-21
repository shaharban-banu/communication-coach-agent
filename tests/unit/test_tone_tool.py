"""
Unit tests for the tone analysis tool.
"""

from unittest.mock import MagicMock, patch

import pytest

from app.core.exceptions import ToolExecutionException
from app.tools.tone import ToneAnalysisTool


@patch("app.tools.tone.Groq")
def test_tone_analysis_success(
    mock_groq: MagicMock,
) -> None:
    """
    Verify successful tone analysis using a mocked Groq response.
    """
    mock_response = MagicMock()

    mock_response.choices[0].message.content = """
    {
        "overall_tone": "frustrated",
        "characteristics": [
            "demanding",
            "impatient"
        ],
        "strengths": [
            "The request is clear."
        ],
        "areas_for_improvement": [
            "Use less confrontational language."
        ],
        "suggested_tone": "professional and assertive"
    }
    """

    mock_groq.return_value.chat.completions.create.return_value = (
        mock_response
    )

    tool = ToneAnalysisTool()

    result = tool.execute(
        "Give me that report immediately."
    )

    assert result["overall_tone"] == "frustrated"
    assert "demanding" in result["characteristics"]
    assert result["suggested_tone"] == (
        "professional and assertive"
    )

    mock_groq.return_value.chat.completions.create.assert_called_once()


@patch("app.tools.tone.Groq")
def test_tone_analysis_empty_message(
    mock_groq: MagicMock,
) -> None:
    """
    Verify that empty input raises a tool execution exception.
    """
    tool = ToneAnalysisTool()

    with pytest.raises(ToolExecutionException):
        tool.execute("")

    mock_groq.return_value.chat.completions.create.assert_not_called()


@patch("app.tools.tone.Groq")
def test_tone_analysis_incomplete_response(
    mock_groq: MagicMock,
) -> None:
    """
    Verify that incomplete LLM output is rejected.
    """
    mock_response = MagicMock()

    mock_response.choices[0].message.content = """
    {
        "overall_tone": "professional"
    }
    """

    mock_groq.return_value.chat.completions.create.return_value = (
        mock_response
    )

    tool = ToneAnalysisTool()

    with pytest.raises(ToolExecutionException):
        tool.execute("Please send the report.")