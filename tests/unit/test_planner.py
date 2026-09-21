"""
Unit tests for the communication planner.
"""

from app.agents.intent import CommunicationIntent
from app.agents.planner import CommunicationPlanner
from app.agents.tool_plan import CommunicationTool


def test_email_writing_workflow() -> None:
    """
    Verify the tool workflow for email writing.
    """
    planner = CommunicationPlanner()

    plan = planner.create_plan(
        CommunicationIntent.EMAIL_WRITING
    )

    assert plan.intent == CommunicationIntent.EMAIL_WRITING

    assert plan.tools == [
        CommunicationTool.EMAIL_GENERATION,
        CommunicationTool.TONE_ANALYSIS,
        CommunicationTool.COMMUNICATION_SCORING,
    ]


def test_grammar_correction_workflow() -> None:
    """
    Verify the tool workflow for grammar correction.
    """
    planner = CommunicationPlanner()

    plan = planner.create_plan(
        CommunicationIntent.GRAMMAR_CORRECTION
    )

    assert plan.tools == [
        CommunicationTool.GRAMMAR_CORRECTION,
        CommunicationTool.COMMUNICATION_SCORING,
    ]


def test_tone_improvement_workflow() -> None:
    """
    Verify that tone improvement uses multiple tools in order.
    """
    planner = CommunicationPlanner()

    plan = planner.create_plan(
        CommunicationIntent.TONE_IMPROVEMENT
    )

    assert plan.tools == [
        CommunicationTool.TONE_ANALYSIS,
        CommunicationTool.CONVERSATION_IMPROVEMENT,
        CommunicationTool.COMMUNICATION_SCORING,
    ]