from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from app.api.dependencies import get_communication_agent
from app.main import app


client = TestClient(app)


@patch("app.api.routes.improve.get_communication_agent")
def test_improve_communication_success(
    mock_create_agent: MagicMock,
) -> None:
    mock_agent = MagicMock()

    mock_agent.process.return_value = {
        "intent": {
            "intent": "tone_improvement",
            "confidence": 0.93,
            "reason": "The user wants to improve the tone.",
        },
        "plan": {
            "intent": "tone_improvement",
            "tools": [
                "tone_analysis",
                "conversation_improvement",
                "communication_scoring",
            ],
            "reason": "Tone improvement workflow.",
        },
        "tool_results": [],
        "response": {
            "feedback": [
                "Use a more polite tone.",
                "Make the request less direct.",
            ],
            "improved_response": (
                "Could you please help me resolve this issue?"
            ),
            "score": 8.5,
        },
    }

    app.dependency_overrides[get_communication_agent] = (
    lambda: mock_agent
)
    try:
        response = client.post(
            "/api/v1/improve",
            json={
                "message": "Fix this problem immediately.",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["improved_response"] == (
            "Could you please help me resolve this issue?"
        )

        assert data["score"] == 8.5

        assert data["feedback"] == [
            "Use a more polite tone.",
            "Make the request less direct.",
        ]

        mock_agent.process.assert_called_once_with(
            message="Fix this problem immediately.",
            context=None,
            session_id=None,
        )
    finally:
        app.dependency_overrides.clear()


def test_improve_communication_empty_message() -> None:
    response = client.post(
        "/api/v1/improve",
        json={
            "message": "",
        },
    )

    assert response.status_code == 422


def test_improve_communication_missing_message() -> None:
    response = client.post(
        "/api/v1/improve",
        json={},
    )

    assert response.status_code == 422