"""
Communication improvement API route.

This module exposes the endpoint used to improve
a user's communication.
"""

from fastapi import APIRouter, Depends

from app.agents.communication_agent import CommunicationAgent
from app.api.dependencies import get_communication_agent
from app.core.logging import get_logger
from app.schemas.api import (
    CommunicationImprovementRequest,
    CommunicationImprovementResponse,
)


logger = get_logger(__name__)

router = APIRouter(
    prefix="/improve",
    tags=["Communication Improvement"],
)

@router.post(
    "",
    response_model=CommunicationImprovementResponse,
)
def improve_communication(
    request: CommunicationImprovementRequest,
    agent: CommunicationAgent = Depends(get_communication_agent),
) -> CommunicationImprovementResponse:
    """
    Improve a user's communication.

    Args:
        request: Communication improvement request.
        agent: Configured communication agent.

    Returns:
        CommunicationImprovementResponse: Improved communication
        and supporting feedback.
    """
    logger.info("Received communication improvement request")

    result = agent.process(
        message=request.message,
        context=request.context,
        session_id=request.session_id,
    )

    response_data = result["response"]

    return CommunicationImprovementResponse(
        improved_response=response_data.get(
            "improved_response"
        ),
        feedback=response_data.get(
            "feedback",
            [],
        ),
        score=response_data.get("score"),
    )