from unittest.mock import MagicMock

import pytest

from app.agents.communication_agent import CommunicationAgent
from app.agents.intent import CommunicationIntent
from app.agents.tool_plan import ToolExecutionPlan, CommunicationTool
from app.core.exceptions import AgentExecutionException
from app.schemas.intent import IntentClassification


def create_agent() -> tuple[
    CommunicationAgent,
    MagicMock,
    MagicMock,
    MagicMock,
    MagicMock,
    MagicMock,
]:
    intent_detector = MagicMock()
    planner = MagicMock()
    tool_executor = MagicMock()
    response_builder=MagicMock()
    memory=MagicMock()

    agent = CommunicationAgent(
        intent_detector=intent_detector,
        planner=planner,
        tool_executor=tool_executor,
        response_builder=response_builder,
        memory=memory,
    )

    return (
        agent,
        intent_detector,
        planner,
        tool_executor,
        response_builder,
        memory
    )


def test_communication_agent_process_success() -> None:
    (
        agent,
        intent_detector,
        planner,
        tool_executor,
        response_builder,
        memory,
    ) = create_agent()

    intent_detector.detect.return_value = IntentClassification(
        intent=CommunicationIntent.GRAMMAR_CORRECTION,
        confidence=0.95,
        reason="The user wants their grammar corrected.",
    )

    plan = ToolExecutionPlan(
        intent=CommunicationIntent.GRAMMAR_CORRECTION,
        tools=[
            CommunicationTool.GRAMMAR_CORRECTION,
            CommunicationTool.COMMUNICATION_SCORING,
        ],
        reason="Grammar correction followed by communication scoring.",
    )

    planner.create_plan.return_value = plan

    response_builder.build.return_value = {
        "feedback": [
            "Grammar improvement: Corrected sentence structure",
            "The communication is clear.",
        ],
        "improved_response": "I would like to request leave.",
        "score": 8.5,
    }

    tool_executor.execute.return_value = [
        {
            "tool": "grammar_correction",
            "result": {
                "corrected_text": "This is a corrected sentence.",
                "changes": ["Grammar corrected"],
            },
        },
        {
            "tool": "communication_scoring",
            "result": {
                "overall_score": 8.5,
            },
        },
    ]

    result = agent.process(
        "Please correct the grammar in this sentence."
    )
    memory.get_history.assert_not_called()
    memory.add_message.assert_not_called()
    assert result["intent"]["intent"] == "grammar_correction"
    assert result["intent"]["confidence"] == 0.95

    assert result["plan"]["intent"] == "grammar_correction"

    assert len(result["tool_results"]) == 2
    

    assert result["response"]["score"] == 8.5

    assert result["response"]["improved_response"] == (
        "I would like to request leave."
    )

    response_builder.build.assert_called_once_with(
        tool_executor.execute.return_value
    )

    intent_detector.detect.assert_called_once_with(
        "Please correct the grammar in this sentence."
    )

    planner.create_plan.assert_called_once_with(
        CommunicationIntent.GRAMMAR_CORRECTION
    )

    tool_executor.execute.assert_called_once_with(
        plan=plan,
        message="Please correct the grammar in this sentence.",
        context=None,
    )


def test_communication_agent_empty_message() -> None:
    (
        agent,
        intent_detector,
        planner,
        tool_executor,
        response_builder,
        memory,
    ) = create_agent()

    with pytest.raises(AgentExecutionException):
        agent.process("")

    memory.get_history.assert_not_called()
    memory.add_message.assert_not_called()
    intent_detector.detect.assert_not_called()
    planner.create_plan.assert_not_called()
    tool_executor.execute.assert_not_called()
    response_builder.build.assert_not_called()

def test_communication_agent_propagates_agent_error() -> None:
    (
        agent,
        intent_detector,
        planner,
        tool_executor,
        response_builder,memory,
    ) = create_agent()

    error = AgentExecutionException(
        "Intent detection failed."
    )

    intent_detector.detect.side_effect = error

    with pytest.raises(AgentExecutionException) as exc_info:
        agent.process("Help me improve this sentence.")

    assert exc_info.value is error

    planner.create_plan.assert_not_called()
    tool_executor.execute.assert_not_called()
    response_builder.build.assert_not_called()
    memory.get_history.assert_not_called()
    memory.add_message.assert_not_called()

def test_communication_agent_uses_memory() -> None:
    (
        agent,
        intent_detector,
        planner,
        tool_executor,
        response_builder,
        memory,
    ) = create_agent()

    intent_detector.detect.return_value = IntentClassification(
        intent=CommunicationIntent.TONE_IMPROVEMENT,
        confidence=0.92,
        reason="The user wants to improve communication tone.",
    )

    plan = ToolExecutionPlan(
        intent=CommunicationIntent.TONE_IMPROVEMENT,
        tools=[
            CommunicationTool.CONVERSATION_IMPROVEMENT,
        ],
        reason="Tone improvement workflow.",
    )

    planner.create_plan.return_value = plan

    tool_executor.execute.return_value = [
        {
            "tool": "conversation_improvement",
            "result": {
                "analysis": "The message is too direct.",
                "suggestions": [
                    "Use a more polite tone."
                ],
                "improved_message": (
                    "Could you please help me with this?"
                ),
            },
        }
    ]

    response_builder.build.return_value = {
        "feedback": [
            "Use a more polite tone."
        ],
        "improved_response": (
            "Could you please help me with this?"
        ),
        "score": None,
    }

    memory.get_history.return_value = [
        {
            "role": "user",
            "content": "I need help with my message.",
        },
        {
            "role": "assistant",
            "content": "Sure, I can help.",
        },
    ]

    result = agent.process(
        message="Make it more polite.",
        session_id="session-123",
    )

    assert result["response"]["improved_response"] == (
        "Could you please help me with this?"
    )

    memory.get_history.assert_called_once_with(
        "session-123"
    )

    assert memory.add_message.call_count == 2

    memory.add_message.assert_any_call(
        session_id="session-123",
        role="user",
        content="Make it more polite.",
    )

    memory.add_message.assert_any_call(
        session_id="session-123",
        role="assistant",
        content="Could you please help me with this?",
    )
