"""
Tool planning models for the communication agent.

This module defines the tools that can be selected by the
communication planner and the execution plan produced from
a detected communication intent.
"""
from enum import Enum
from pydantic import BaseModel,Field
from app.agents.intent import CommunicationIntent

class CommunicationTool(str,Enum):
    """
    Reusable communication capabilities available to the agent.
    """

    GRAMMAR_CORRECTION = "grammar_correction"
    TONE_ANALYSIS = "tone_analysis"
    EMAIL_GENERATION = "email_generation"
    INTERVIEW_COACHING = "interview_coaching"
    CONVERSATION_IMPROVEMENT = "conversation_improvement"
    COMMUNICATION_SCORING = "communication_scoring"

class ToolExecutionPlan(BaseModel):
    """
    Execution plan generated for a communication request.

    Attributes:
        intent: Primary communication intent.
        tools: Ordered list of tools to execute.
        reason: Explanation for the selected workflow.
    """

    intent: CommunicationIntent

    tools: list[CommunicationTool] = Field(default_factory=list,min_length=1,)

    reason: str = Field(min_length=1,)