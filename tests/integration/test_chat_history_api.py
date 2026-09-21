from fastapi.testclient import TestClient

from app.api.dependencies import get_communication_agent
from app.main import app


client = TestClient(app)


def test_get_chat_history() -> None:
    mock_agent = type("MockAgent", (), {})()
    mock_agent.memory = type("MockMemory", (), {})()

    mock_agent.memory.get_history = lambda session_id: [
        {
            "role": "user",
            "content": "Make this more professional.",
        },
        {
            "role": "assistant",
            "content": "Could you please make this more professional?",
        },
    ]

    app.dependency_overrides[get_communication_agent] = (
        lambda: mock_agent
    )

    try:
        response = client.get(
            "/api/v1/chat-history/session-123"
        )

        assert response.status_code == 200

        data = response.json()

        assert data["messages"] == [
            {
                "role": "user",
                "content": "Make this more professional.",
            },
            {
                "role": "assistant",
                "content": (
                    "Could you please make this more professional?"
                ),
            },
        ]

    finally:
        app.dependency_overrides.clear()


def test_get_chat_history_empty_session() -> None:
    mock_agent = type("MockAgent", (), {})()
    mock_agent.memory = type("MockMemory", (), {})()

    mock_agent.memory.get_history = lambda session_id: []

    app.dependency_overrides[get_communication_agent] = (
        lambda: mock_agent
    )

    try:
        response = client.get(
            "/api/v1/chat-history/unknown-session"
        )

        assert response.status_code == 200
        assert response.json() == {"messages": []}

    finally:
        app.dependency_overrides.clear()