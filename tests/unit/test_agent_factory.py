from unittest.mock import patch

from app.agents.communication_agent import CommunicationAgent
from app.agents.factory import create_communication_agent


@patch("app.agents.factory.create_tool_registry")
@patch("app.agents.factory.IntentDetector")
def test_create_communication_agent(
    mock_intent_detector,
    mock_create_registry,
) -> None:
    mock_registry = mock_create_registry.return_value

    agent = create_communication_agent()

    assert isinstance(agent, CommunicationAgent)

    mock_create_registry.assert_called_once()
    mock_intent_detector.assert_called_once()