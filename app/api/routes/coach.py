"""
Communication coaching API route.

This module exposes the endpoint used to provide
AI-powered communication coaching.
"""

from fastapi import APIRouter, Depends

from app.agents.communication_agent import CommunicationAgent
from app.api.dependencies import get_communication_agent
from app.core.logging import get_logger
from app.schemas.api import (
    CoachingRequest,
    CoachingResponse,
)


logger = get_logger(__name__)

router = APIRouter(
    prefix="/coach",
    tags=["Communication Coaching"],
)


@router.post(
    "",
    response_model=CoachingResponse,
)
def coach_communication(
    request: CoachingRequest,
    agent: CommunicationAgent = Depends(get_communication_agent),
) -> CoachingResponse:
    """
    Provide AI-powered communication coaching.

    Args:
        request: Communication coaching request.
        agent: Configured communication agent.

    Returns:
        CoachingResponse: Coaching feedback and improved response.
    """
    logger.info("Received communication coaching request")

    result = agent.process(
        message=request.message,
        context=request.context,
        session_id=request.session_id,
    )

    intent_data = result["intent"]
    response_data = result["response"]

    return CoachingResponse(
        intent=intent_data["intent"],
        feedback=response_data.get("feedback", []),
        improved_response=response_data.get(
            "improved_response"
        ),
        score=response_data.get("score"),
    )