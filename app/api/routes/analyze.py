"""
Communication analysis API route.

This module exposes the endpoint used to analyze
a user's communication request.
"""

from fastapi import APIRouter, Depends

from app.agents.communication_agent import CommunicationAgent

from app.core.logging import get_logger
from app.schemas.api import (
    CommunicationAnalysisRequest,
    CommunicationAnalysisResponse,
)
from app.api.dependencies import get_communication_agent


logger = get_logger(__name__)

router = APIRouter(
    prefix="/analyze",
    tags=["Communication Analysis"],
)

@router.post(
    "",
    response_model=CommunicationAnalysisResponse,
)
def analyze_communication(
    request: CommunicationAnalysisRequest,
    agent: CommunicationAgent = Depends(get_communication_agent),
) -> CommunicationAnalysisResponse:
    """
    Analyze a user's communication request.

    Args:
        request: Communication analysis request.
        agent: Configured communication agent.

    Returns:
        CommunicationAnalysisResponse: Communication analysis result.
    """
    logger.info("Received communication analysis request")

    result = agent.process(
        message=request.message,
        context=request.context,
        session_id=request.session_id,
    )

    intent_data = result["intent"]
    response_data = result["response"]

    return CommunicationAnalysisResponse(
        intent=intent_data["intent"],
        confidence=intent_data["confidence"],
        reason=intent_data["reason"],
        score=response_data.get("score"),
        feedback=response_data.get("feedback", []),
    )