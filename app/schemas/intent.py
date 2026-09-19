"""
Schemas for LLM-based communication intent classification.
"""

from pydantic import BaseModel, Field,ConfigDict

from app.agents.intent import CommunicationIntent


class IntentClassification(BaseModel):
    """
    Structured result returned by the intent classifier.

    Attributes:
        intent: Primary communication intent identified by the LLM.
        confidence: Confidence score between 0 and 1.
        reason: Brief explanation for the classification.
    """
    model_config=ConfigDict(extra="forbid")

    intent: CommunicationIntent = Field(
        description="Primary communication intent.",
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1.",
    )

    reason: str = Field(
        min_length=1,
        description="Brief explanation for the selected intent.",
    )