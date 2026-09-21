"""
Chat history API routes.

This module exposes endpoints for retrieving short-term
conversation history.
"""

from fastapi import APIRouter, Depends

from app.api.dependencies import get_communication_agent
from app.agents.communication_agent import CommunicationAgent
from app.schemas.api import ChatHistoryMessage, ChatHistoryResponse

router = APIRouter(
    prefix="/chat-history",
    tags=["Chat History"],
)


@router.get(
    "/{session_id}",
    response_model=ChatHistoryResponse,
)
def get_chat_history(
    session_id: str,
    agent: CommunicationAgent = Depends(get_communication_agent),
) -> ChatHistoryResponse:
    """
    Return the conversation history for a session.

    Args:
        session_id: Unique conversation session identifier.
        agent: Shared communication agent.

    Returns:
        ChatHistoryResponse: Messages stored for the session.
    """
    history = agent.memory.get_history(session_id)

    messages = [
        ChatHistoryMessage(**message)
        for message in history
    ]

    return ChatHistoryResponse(messages=messages)