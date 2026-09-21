"""
Unit tests for the email generation tool.
"""

from unittest.mock import MagicMock, patch

import pytest

from app.core.exceptions import ToolExecutionException
from app.tools.email import EmailGenerationTool


@patch("app.tools.email.Groq")
def test_email_generation_success(
    mock_groq: MagicMock,
) -> None:
    """
    Verify successful email generation.
    """
    mock_response = MagicMock()

    mock_response.choices[0].message.content = """
    {
        "subject": "Leave Request",
        "body": "Dear Manager,\\n\\nI would like to request two days of leave.\\n\\nRegards",
        "tone": "professional"
    }
    """

    mock_groq.return_value.chat.completions.create.return_value = (
        mock_response
    )

    tool = EmailGenerationTool()

    result = tool.execute(
        "Write an email requesting two days leave."
    )

    assert result["subject"] == "Leave Request"
    assert "two days" in result["body"]
    assert result["tone"] == "professional"

    mock_groq.return_value.chat.completions.create.assert_called_once()


@patch("app.tools.email.Groq")
def test_email_generation_empty_message(
    mock_groq: MagicMock,
) -> None:
    """
    Verify that empty input is rejected.
    """
    tool = EmailGenerationTool()

    with pytest.raises(ToolExecutionException):
        tool.execute("")

    mock_groq.return_value.chat.completions.create.assert_not_called()


@patch("app.tools.email.Groq")
def test_email_generation_incomplete_response(
    mock_groq: MagicMock,
) -> None:
    """
    Verify that incomplete LLM output is rejected.
    """
    mock_response = MagicMock()

    mock_response.choices[0].message.content = """
    {
        "subject": "Leave Request"
    }
    """

    mock_groq.return_value.chat.completions.create.return_value = (
        mock_response
    )

    tool = EmailGenerationTool()

    with pytest.raises(ToolExecutionException):
        tool.execute(
            "Write an email requesting leave."
        )