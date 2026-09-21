from app.agents.tool_plan import CommunicationTool
from app.tools.factory import create_tool_registry


def test_create_tool_registry() -> None:
    registry = create_tool_registry()

    expected_tools = {
        CommunicationTool.GRAMMAR_CORRECTION,
        CommunicationTool.TONE_ANALYSIS,
        CommunicationTool.EMAIL_GENERATION,
        CommunicationTool.INTERVIEW_COACHING,
        CommunicationTool.CONVERSATION_IMPROVEMENT,
        CommunicationTool.COMMUNICATION_SCORING,
    }

    for tool_type in expected_tools:
        tool = registry.get(tool_type)
        assert tool.tool_type == tool_type