from unittest.mock import MagicMock, patch

import pytest

from app.core.exceptions import ToolExecutionException
from app.tools.scoring import CommunicationScoringTool


@patch("app.tools.scoring.Groq")
def test_communication_scoring_success(
    mock_groq: MagicMock,
) -> None:
    mock_response = MagicMock()

    mock_response.choices[0].message.content = """
    {
        "grammar": 8.5,
        "clarity": 8.0,
        "tone": 9.0,
        "professionalism": 8.5,
        "overall_score": 8.5,
        "feedback": "The communication is clear and professional.",
        "improvement_priorities": [
            "Use more concise sentences"
        ]
    }
    """

    mock_groq.return_value.chat.completions.create.return_value = (
        mock_response
    )

    tool = CommunicationScoringTool()

    result = tool.execute(
        "I would like to discuss the project requirements."
    )

    assert result["grammar"] == 8.5
    assert result["clarity"] == 8.0
    assert result["tone"] == 9.0
    assert result["professionalism"] == 8.5
    assert result["overall_score"] == 8.5

    assert "feedback" in result
    assert len(result["improvement_priorities"]) > 0

    mock_groq.return_value.chat.completions.create.assert_called_once()


@patch("app.tools.scoring.Groq")
def test_communication_scoring_empty_message(
    mock_groq: MagicMock,
) -> None:
    tool = CommunicationScoringTool()

    with pytest.raises(ToolExecutionException):
        tool.execute("")

    mock_groq.return_value.chat.completions.create.assert_not_called()


@patch("app.tools.scoring.Groq")
def test_communication_scoring_incomplete_response(
    mock_groq: MagicMock,
) -> None:
    mock_response = MagicMock()

    mock_response.choices[0].message.content = """
    {
        "grammar": 8.0,
        "clarity": 7.0
    }
    """

    mock_groq.return_value.chat.completions.create.return_value = (
        mock_response
    )

    tool = CommunicationScoringTool()

    with pytest.raises(ToolExecutionException):
        tool.execute(
            "Please evaluate my communication."
        )


@patch("app.tools.scoring.Groq")
def test_communication_scoring_invalid_score(
    mock_groq: MagicMock,
) -> None:
    mock_response = MagicMock()

    mock_response.choices[0].message.content = """
    {
        "grammar": 15.0,
        "clarity": 7.0,
        "tone": 8.0,
        "professionalism": 8.0,
        "overall_score": 9.0,
        "feedback": "Good communication.",
        "improvement_priorities": []
    }
    """

    mock_groq.return_value.chat.completions.create.return_value = (
        mock_response
    )

    tool = CommunicationScoringTool()

    with pytest.raises(ToolExecutionException):
        tool.execute(
            "Please score this communication."
        )