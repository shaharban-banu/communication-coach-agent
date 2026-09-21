import pytest
from pydantic import ValidationError

from app.agents.intent import CommunicationIntent
from app.schemas.api import (
    ChatHistoryResponse,
    CommunicationAnalysisRequest,
    CommunicationAnalysisResponse,
    CommunicationImprovementRequest,
    CommunicationImprovementResponse,
    CoachingRequest,
    CoachingResponse,
)


def test_analysis_request_valid() -> None:
    request = CommunicationAnalysisRequest(
        message="Please analyze my communication."
    )

    assert request.message == (
        "Please analyze my communication."
    )
    assert request.context is None


def test_analysis_request_empty_message() -> None:
    with pytest.raises(ValidationError):
        CommunicationAnalysisRequest(message="")


def test_analysis_response_valid() -> None:
    response = CommunicationAnalysisResponse(
        intent=CommunicationIntent.GRAMMAR_CORRECTION,
        confidence=0.95,
        reason="Grammar correction requested.",
        score=8.5,
        feedback=["Improve sentence structure."],
    )

    assert response.intent == (
        CommunicationIntent.GRAMMAR_CORRECTION
    )
    assert response.confidence == 0.95
    assert response.score == 8.5


def test_coaching_request_valid() -> None:
    request = CoachingRequest(
        message="Help me answer this interview question."
    )

    assert request.message.startswith("Help me")


def test_coaching_response_valid() -> None:
    response = CoachingResponse(
        intent=CommunicationIntent.INTERVIEW_PRACTICE,
        feedback=["Use the STAR method."],
        improved_response="A structured interview answer.",
        score=8.0,
    )

    assert response.intent == (
        CommunicationIntent.INTERVIEW_PRACTICE
    )
    assert response.score == 8.0


def test_improvement_request_valid() -> None:
    request = CommunicationImprovementRequest(
        message="Please improve this message."
    )

    assert request.context is None


def test_improvement_response_valid() -> None:
    response = CommunicationImprovementResponse(
        improved_response="Could you please help me?",
        feedback=["Use a more polite tone."],
        score=8.5,
    )

    assert response.improved_response == (
        "Could you please help me?"
    )


def test_chat_history_response() -> None:
    response = ChatHistoryResponse(
        messages=[
            {
                "role": "user",
                "content": "Hello",
            },
            {
                "role": "assistant",
                "content": "How can I help?",
            },
        ]
    )

    assert len(response.messages) == 2
    assert response.messages[0].role == "user"

def test_analysis_request_accepts_session_id() -> None:
    request = CommunicationAnalysisRequest(
        message="Make this professional.",
        session_id="session-123",
    )

    assert request.session_id == "session-123"


def test_coaching_request_accepts_session_id() -> None:
    request = CoachingRequest(
        message="Help me answer this interview question.",
        session_id="session-123",
    )

    assert request.session_id == "session-123"


def test_improvement_request_accepts_session_id() -> None:
    request = CommunicationImprovementRequest(
        message="Make this more polite.",
        session_id="session-123",
    )

    assert request.session_id == "session-123"