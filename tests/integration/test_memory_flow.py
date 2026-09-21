from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.api.dependencies import get_communication_agent
from app.main import app


client = TestClient(app)


def test_conversation_memory_flow() -> None:
    mock_agent = MagicMock()

    first_result = {
        "intent": {
            "intent": "tone_improvement",
            "confidence": 0.95,
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
            "feedback": ["Use a more polite tone."],
            "improved_response": "Could you please help me with this?",
            "score": 8.5,
        },
    }

    second_result = {
        "intent": {
            "intent": "tone_improvement",
            "confidence": 0.94,
            "reason": "The user wants to refine the previous message.",
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
            "feedback": ["Make the request shorter."],
            "improved_response": "Could you help me with this?",
            "score": 9.0,
        },
    }

    mock_agent.process.side_effect = [
        first_result,
        second_result,
    ]

    mock_agent.memory.get_history.return_value = [
        {
            "role": "user",
            "content": "Make this more polite.",
        },
        {
            "role": "assistant",
            "content": "Could you please help me with this?",
        },
    ]

    app.dependency_overrides[get_communication_agent] = (
        lambda: mock_agent
    )

    try:
        first_response = client.post(
            "/api/v1/coach",
            json={
                "message": "Make this more polite.",
                "session_id": "session-123",
            },
        )

        assert first_response.status_code == 200

        second_response = client.post(
            "/api/v1/coach",
            json={
                "message": "Can you make it shorter?",
                "session_id": "session-123",
            },
        )

        assert second_response.status_code == 200

        mock_agent.process.assert_any_call(
            message="Make this more polite.",
            context=None,
            session_id="session-123",
        )

        mock_agent.process.assert_any_call(
            message="Can you make it shorter?",
            context=None,
            session_id="session-123",
        )

        history_response = client.get(
            "/api/v1/chat-history/session-123"
        )

        assert history_response.status_code == 200

        assert history_response.json()["messages"] == [
            {
                "role": "user",
                "content": "Make this more polite.",
            },
            {
                "role": "assistant",
                "content": "Could you please help me with this?",
            },
        ]

    finally:
        app.dependency_overrides.clear()