"""
API request and response schemas.

This module defines the data contracts used by the
Communication Coach Agent REST API.
"""

from pydantic import BaseModel, Field

from app.agents.intent import CommunicationIntent


class CommunicationAnalysisRequest(BaseModel):
    """
    Request schema for communication analysis.
    """

    message: str = Field(
        ...,
        min_length=1,
        description="Communication text to analyze.",
    )

    context: str | None = Field(
        default=None,
        description="Optional context for the analysis.",
    )
    session_id: str | None = Field(
        default=None,
        min_length=1,
        description="Optional conversation session identifier.",
    )


class CommunicationAnalysisResponse(BaseModel):
    """
    Response schema for communication analysis.
    """

    intent: CommunicationIntent
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )
    reason: str
    score: float | None = None
    feedback: list[str] = Field(
        default_factory=list,
    )


class CoachingRequest(BaseModel):
    """
    Request schema for communication coaching.
    """

    message: str = Field(
        ...,
        min_length=1,
        description="User communication or coaching request.",
    )

    context: str | None = Field(
        default=None,
        description="Optional context for coaching.",
    )
    session_id: str | None = Field(
        default=None,
        min_length=1,
        description="Optional conversation session identifier.",
    )


class CoachingResponse(BaseModel):
    """
    Response schema for communication coaching.
    """

    intent: CommunicationIntent
    feedback: list[str] = Field(
        default_factory=list,
    )
    improved_response: str | None = None
    score: float | None = None


class CommunicationImprovementRequest(BaseModel):
    """
    Request schema for communication improvement.
    """

    message: str = Field(
        ...,
        min_length=1,
        description="Communication text to improve.",
    )

    context: str | None = Field(
        default=None,
        description="Optional context for improvement.",
    )
    session_id: str | None = Field(
        default=None,
        min_length=1,
        description="Optional conversation session identifier.",
    )


class CommunicationImprovementResponse(BaseModel):
    """
    Response schema for communication improvement.
    """

    improved_response: str | None = None
    feedback: list[str] = Field(
        default_factory=list,
    )
    score: float | None = None


class ChatHistoryMessage(BaseModel):
    """
    Represents one message stored in conversational history.
    """

    role: str
    content: str


class ChatHistoryResponse(BaseModel):
    """
    Response schema for chat history.
    """

    messages: list[ChatHistoryMessage] = Field(
        default_factory=list,
    )

class MetricsResponse(BaseModel):
    """API monitoring metrics."""

    total_requests: int
    successful_requests: int
    failed_requests: int
    error_rate: float
    average_response_time: float