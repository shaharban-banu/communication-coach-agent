"""
Communication agent factory.

This module creates the fully configured CommunicationAgent
and its required dependencies.
"""

from app.agents.communication_agent import CommunicationAgent
from app.agents.intent_detector import IntentDetector
from app.agents.planner import CommunicationPlanner
from app.agents.response_builder import CommunicationResponseBuilder
from app.core.logging import get_logger
from app.tools.executor import ToolExecutor
from app.tools.factory import create_tool_registry
from app.memory.conversation import ConversationMemory


logger = get_logger(__name__)


def create_communication_agent() -> CommunicationAgent:
    """
    Create a fully configured communication agent.

    Returns:
        CommunicationAgent: Configured communication agent with
        intent detection, planning, tool execution, and response
        building capabilities.
    """
    intent_detector = IntentDetector()
    planner = CommunicationPlanner()

    tool_registry = create_tool_registry()
    tool_executor = ToolExecutor(tool_registry)

    response_builder = CommunicationResponseBuilder()
    memory=ConversationMemory()

    agent = CommunicationAgent(
        intent_detector=intent_detector,
        planner=planner,
        tool_executor=tool_executor,
        response_builder=response_builder,
        memory=memory,
    )

    logger.info("Communication agent created successfully")

    return agent