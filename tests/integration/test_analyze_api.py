from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.agents.intent import CommunicationIntent
from app.main import app
from app.api.dependencies import get_communication_agent


client = TestClient(app)


@patch("app.api.routes.analyze.get_communication_agent")
def test_analyze_communication_success(
    mock_create_agent: MagicMock,
) -> None:
    mock_agent = MagicMock()

    mock_agent.process.return_value = {
        "intent": {
            "intent": CommunicationIntent.GRAMMAR_CORRECTION.value,
            "confidence": 0.95,
            "reason": "The user wants grammar correction.",
        },
        "plan": {
            "intent": CommunicationIntent.GRAMMAR_CORRECTION.value,
            "tools": ["grammar_correction"],
            "reason": "Grammar correction workflow.",
        },
        "tool_results": [],
        "response": {
            "feedback": [
                "Improve sentence structure."
            ],
            "improved_response": (
                "This is the corrected sentence."
            ),
            "score": 8.5,
        },
    }

    app.dependency_overrides[get_communication_agent] = (
        lambda: mock_agent
    )
    try:
        response = client.post(
            "/api/v1/analyze",
            json={
                "message": "Please correct my grammar.",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["intent"] == "grammar_correction"
        assert data["confidence"] == 0.95
        assert data["score"] == 8.5
        assert data["feedback"] == [
            "Improve sentence structure."
        ]

        mock_agent.process.assert_called_once_with(
            message="Please correct my grammar.",
            context=None,
            session_id=None,
        )
    finally:
        app.dependency_overrides.clear()

def test_analyze_communication_empty_message() -> None:
    response = client.post(
        "/api/v1/analyze",
        json={
            "message": "",
        },
    )

    assert response.status_code == 422


def test_analyze_communication_missing_message() -> None:
    response = client.post(
        "/api/v1/analyze",
        json={},
    )

    assert response.status_code == 422