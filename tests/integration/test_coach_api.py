from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.agents.intent import CommunicationIntent
from app.main import app
from app.api.dependencies import get_communication_agent


client = TestClient(app)


@patch("app.api.routes.coach.get_communication_agent")
def test_coach_communication_success(
    mock_create_agent: MagicMock,
) -> None:
    mock_agent = MagicMock()

    mock_agent.process.return_value = {
        "intent": {
            "intent": CommunicationIntent.INTERVIEW_PRACTICE.value,
            "confidence": 0.94,
            "reason": "The user is practicing for an interview.",
        },
        "plan": {
            "intent": CommunicationIntent.INTERVIEW_PRACTICE.value,
            "tools": [
                "interview_coaching",
                "communication_scoring",
            ],
            "reason": "Interview coaching workflow.",
        },
        "tool_results": [],
        "response": {
            "feedback": [
                "Use the STAR method.",
                "Give a specific example.",
            ],
            "improved_response": (
                "A stronger answer would describe "
                "the situation, task, action, and result."
            ),
            "score": 8.0,
        },
    }

    app.dependency_overrides[get_communication_agent] = (
        lambda: mock_agent
    )


    # mock_create_agent.return_value = mock_agent
    try:
        response = client.post(
            "/api/v1/coach",
            json={
                "message": (
                    "How should I answer: "
                    "Tell me about a challenging project?"
                ),
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["intent"] == "interview_practice"
        assert data["score"] == 8.0

        assert data["feedback"] == [
            "Use the STAR method.",
            "Give a specific example.",
        ]

        assert data["improved_response"] is not None

        mock_agent.process.assert_called_once_with(
            message=(
                "How should I answer: "
                "Tell me about a challenging project?"
            ),
            context=None,
            session_id=None,
        )
    finally:
        app.dependency_overrides.clear()

def test_coach_communication_empty_message() -> None:
    response = client.post(
        "/api/v1/coach",
        json={
            "message": "",
        },
    )

    assert response.status_code == 422


def test_coach_communication_missing_message() -> None:
    response = client.post(
        "/api/v1/coach",
        json={},
    )

    assert response.status_code == 422