"""
Unit tests for communication intent classification schemas.
"""

import pytest
from pydantic import ValidationError

from app.agents.intent import CommunicationIntent
from app.schemas.intent import IntentClassification


def test_valid_intent_classification() -> None:
    """
    Verify that a valid intent classification is accepted.
    """
    result = IntentClassification(
        intent=CommunicationIntent.TONE_IMPROVEMENT,
        confidence=0.95,
        reason="The user wants to improve the tone.",
    )

    assert result.intent == CommunicationIntent.TONE_IMPROVEMENT
    assert result.confidence == 0.95


def test_confidence_cannot_exceed_one() -> None:
    """
    Verify that confidence values above one are rejected.
    """
    with pytest.raises(ValidationError):
        IntentClassification(
            intent=CommunicationIntent.EMAIL_WRITING,
            confidence=1.5,
            reason="Invalid confidence.",
        )


def test_confidence_cannot_be_negative() -> None:
    """
    Verify that negative confidence values are rejected.
    """
    with pytest.raises(ValidationError):
        IntentClassification(
            intent=CommunicationIntent.EMAIL_WRITING,
            confidence=-0.1,
            reason="Invalid confidence.",
        )


def test_unknown_fields_are_rejected() -> None:
    """
    Verify that unexpected fields are rejected by the schema.
    """
    with pytest.raises(ValidationError):
        IntentClassification(
            intent=CommunicationIntent.EMAIL_WRITING,
            confidence=0.9,
            reason="Valid classification.",
            unexpected_field="not allowed",
        )