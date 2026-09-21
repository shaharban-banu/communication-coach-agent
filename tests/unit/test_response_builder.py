import pytest

from app.agents.response_builder import CommunicationResponseBuilder
from app.core.exceptions import AgentExecutionException


def test_response_builder_with_grammar_and_score() -> None:
    builder = CommunicationResponseBuilder()

    tool_results = [
        {
            "tool": "grammar_correction",
            "result": {
                "corrected_text": "I would like to request leave.",
                "changes": [
                    "Corrected sentence structure"
                ],
            },
        },
        {
            "tool": "communication_scoring",
            "result": {
                "overall_score": 8.5,
                "feedback": "The communication is clear.",
                "improvement_priorities": [
                    "Use more concise sentences"
                ],
            },
        },
    ]

    result = builder.build(tool_results)

    assert result["score"] == 8.5

    assert (
        "Grammar improvement: Corrected sentence structure"
        in result["feedback"]
    )

    assert (
        "The communication is clear."
        in result["feedback"]
    )

    assert (
        "Improvement priority: Use more concise sentences"
        in result["feedback"]
    )


def test_response_builder_with_email() -> None:
    builder = CommunicationResponseBuilder()

    tool_results = [
        {
            "tool": "email_generation",
            "result": {
                "subject": "Leave Request",
                "body": "Dear Manager,\n\nI would like to request leave.",
                "tone": "professional",
            },
        }
    ]

    result = builder.build(tool_results)

    assert result["improved_response"] == (
        "Subject: Leave Request\n\n"
        "Dear Manager,\n\n"
        "I would like to request leave."
    )


def test_response_builder_with_conversation_improvement() -> None:
    builder = CommunicationResponseBuilder()

    tool_results = [
        {
            "tool": "conversation_improvement",
            "result": {
                "analysis": "The original message is too direct.",
                "suggestions": [
                    "Use a more polite tone."
                ],
                "improved_message": (
                    "Could you please help me with this issue?"
                ),
            },
        }
    ]

    result = builder.build(tool_results)

    assert result["improved_response"] == (
        "Could you please help me with this issue?"
    )

    assert (
        "Communication analysis: "
        "The original message is too direct."
        in result["feedback"]
    )


def test_response_builder_empty_results() -> None:
    builder = CommunicationResponseBuilder()

    with pytest.raises(AgentExecutionException):
        builder.build([])