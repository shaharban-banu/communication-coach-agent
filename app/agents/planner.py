"""
Communication planning logic.

This module converts a detected communication intent into an
ordered execution plan of reusable communication tools.
"""
from app.agents.intent import CommunicationIntent
from app.agents.tool_plan import (CommunicationTool,ToolExecutionPlan)
from app.core.logging import get_logger

logger=get_logger(__name__)

class CommunicationPlanner:
    """
    Create an ordered tool execution plan from a communication intent.

    The planner currently uses deterministic workflow rules. The
    intent itself is detected using the Groq LLM, while this component
    is responsible for translating that intent into executable tools.
    """
    _WORKFLOWS:dict[CommunicationIntent,tuple[CommunicationTool,...],]={
            CommunicationIntent.EMAIL_WRITING: (
            CommunicationTool.EMAIL_GENERATION,
            CommunicationTool.TONE_ANALYSIS,
            CommunicationTool.COMMUNICATION_SCORING,
        ),
        CommunicationIntent.INTERVIEW_PRACTICE: (
            CommunicationTool.INTERVIEW_COACHING,
            CommunicationTool.COMMUNICATION_SCORING,
        ),
        CommunicationIntent.GRAMMAR_CORRECTION: (
            CommunicationTool.GRAMMAR_CORRECTION,
            CommunicationTool.COMMUNICATION_SCORING,
        ),
        CommunicationIntent.TONE_IMPROVEMENT: (
            CommunicationTool.TONE_ANALYSIS,
            CommunicationTool.CONVERSATION_IMPROVEMENT,
            CommunicationTool.COMMUNICATION_SCORING,
        ),
        CommunicationIntent.PUBLIC_SPEAKING: (
            CommunicationTool.CONVERSATION_IMPROVEMENT,
            CommunicationTool.COMMUNICATION_SCORING,
        ),
        CommunicationIntent.CONFLICT_RESOLUTION: (
            CommunicationTool.TONE_ANALYSIS,
            CommunicationTool.CONVERSATION_IMPROVEMENT,
            CommunicationTool.COMMUNICATION_SCORING,
        ),
        CommunicationIntent.CUSTOMER_COMMUNICATION: (
            CommunicationTool.TONE_ANALYSIS,
            CommunicationTool.CONVERSATION_IMPROVEMENT,
            CommunicationTool.COMMUNICATION_SCORING,
        ),
    }

    def create_plan(self,intent:CommunicationIntent,):

        """
        Create a tool execution plan for a detected intent.

        Args:
            intent: Primary communication intent.

        Returns:
            ToolExecutionPlan: Ordered tools required for the intent.
        """
        tools=self._WORKFLOWS.get(intent)
        if tools is None:
            logger.error("No workflows configured for intent = %s",intent.value,)
            raise ValueError(
                f"no workflow configured for intent :{intent.value}"
            )
        logger.info("communication plan created | intent =%s |tool= %s",
                    intent.value,[tool.value for tool in tools],)
        return ToolExecutionPlan(
            intent=intent,
            tools=list(tools),
            reason=self._build_reason(intent,tools)
        )

    @staticmethod
    def _build_reason(intent:CommunicationIntent,tools:tuple[CommunicationTool,...],):
        """
        Build a human-readable explanation of the selected workflow.

        Args:
            intent: Communication intent.
            tools: Ordered tools selected for the intent.

        Returns:
            str: Explanation of the execution workflow.
        """
        tool_names=",".join(tool.value for tool in tools)
        return(
            f"The {intent.value} workflow uses the following tools "
            f"in sequence : {tool_names}."
        )
   