from unittest.mock import MagicMock, patch

import pytest

from app.core.exceptions import ToolExecutionException
from app.tools.conversation import ConversationImprovementTool


@patch("app.tools.conversation.Groq")
def test_conversation_improvement_success(
    mock_groq: MagicMock,
) -> None:
    mock_response = MagicMock()

    mock_response.choices[0].message.content = """
    {
        "analysis": "The message sounds slightly direct.",
        "issues": [
            "The tone could be softer",
            "The request could be clearer"
        ],
        "suggestions": [
            "Use a more respectful opening"
        ],
        "improved_message": "Could you please help me with this issue?",
        "recommended_tone": "polite and professional"
    }
    """

    mock_groq.return_value.chat.completions.create.return_value = (
        mock_response
    )

    tool = ConversationImprovementTool()

    result = tool.execute(
        "You need to fix this problem immediately."
    )

    assert "analysis" in result
    assert len(result["issues"]) > 0
    assert len(result["suggestions"]) > 0
    assert "improved_message" in result
    assert result["recommended_tone"] == "polite and professional"

    mock_groq.return_value.chat.completions.create.assert_called_once()


@patch("app.tools.conversation.Groq")
def test_conversation_improvement_empty_message(
    mock_groq: MagicMock,
) -> None:
    tool = ConversationImprovementTool()

    with pytest.raises(ToolExecutionException):
        tool.execute("")

    mock_groq.return_value.chat.completions.create.assert_not_called()


@patch("app.tools.conversation.Groq")
def test_conversation_improvement_incomplete_response(
    mock_groq: MagicMock,
) -> None:
    mock_response = MagicMock()

    mock_response.choices[0].message.content = """
    {
        "analysis": "The message needs improvement."
    }
    """

    mock_groq.return_value.chat.completions.create.return_value = (
        mock_response
    )

    tool = ConversationImprovementTool()

    with pytest.raises(ToolExecutionException):
        tool.execute(
            "Please improve this communication."
        )