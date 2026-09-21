"""
Tool registry factory.

This module creates the application's default tool registry
with all currently available communication tools.
"""

from app.core.logging import get_logger
from app.tools.email import EmailGenerationTool
from app.tools.grammar import GrammarCorrectionTool
from app.tools.interview import InterviewCoachingTool
from app.tools.scoring import CommunicationScoringTool
from app.tools.tone import ToneAnalysisTool
from app.tools.conversation import ConversationImprovementTool
from app.tools.registry import ToolRegistry

logger = get_logger(__name__)


def create_tool_registry() -> ToolRegistry:
    """
    Create and configure the application tool registry.

    Returns:
        ToolRegistry: Registry containing available communication tools.
    """
    registry = ToolRegistry()

    tools = [
        GrammarCorrectionTool(),
        ToneAnalysisTool(),
        EmailGenerationTool(),
        InterviewCoachingTool(),
        ConversationImprovementTool(),
        CommunicationScoringTool(),
    ]

    for tool in tools:
        registry.register(tool)

    logger.info("Application tool registry created")

    return registry