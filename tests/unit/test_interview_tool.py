from unittest.mock import MagicMock, patch

import pytest

from app.core.exceptions import ToolExecutionException
from app.tools.interview import InterviewCoachingTool


@patch("app.tools.interview.Groq")
def test_interview_coaching_success(mock_groq: MagicMock) -> None:
    mock_response = MagicMock()

    mock_response.choices[0].message.content = """
    {
        "assessment": "The answer is relevant but could be more structured.",
        "strengths": [
            "Relevant experience",
            "Clear explanation"
        ],
        "areas_for_improvement": [
            "Use a structured format"
        ],
        "suggestions": [
            "Use the STAR method"
        ],
        "improved_answer": "A stronger answer would follow the STAR structure."
    }
    """

    mock_groq.return_value.chat.completions.create.return_value = (
        mock_response
    )

    tool = InterviewCoachingTool()

    result = tool.execute(
        "Tell me about a challenging project you worked on."
    )

    assert "assessment" in result
    assert len(result["strengths"]) > 0
    assert len(result["areas_for_improvement"]) > 0
    assert len(result["suggestions"]) > 0
    assert "STAR" in result["improved_answer"]

    mock_groq.return_value.chat.completions.create.assert_called_once()


@patch("app.tools.interview.Groq")
def test_interview_coaching_empty_message(
    mock_groq: MagicMock,
) -> None:
    tool = InterviewCoachingTool()

    with pytest.raises(ToolExecutionException):
        tool.execute("")

    mock_groq.return_value.chat.completions.create.assert_not_called()


@patch("app.tools.interview.Groq")
def test_interview_coaching_incomplete_response(
    mock_groq: MagicMock,
) -> None:
    mock_response = MagicMock()

    mock_response.choices[0].message.content = """
    {
        "assessment": "The answer needs improvement."
    }
    """

    mock_groq.return_value.chat.completions.create.return_value = (
        mock_response
    )

    tool = InterviewCoachingTool()

    with pytest.raises(ToolExecutionException):
        tool.execute(
            "Tell me about yourself."
        )