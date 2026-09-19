"""
Communication intent definitions.

This module defines the supported communication intents used by
the agentic decision-making pipeline.
"""
from enum import Enum

class CommunicationIntent(str,Enum):
    """
    Supported communication use cases.

    Each intent represents the primary goal identified from a user's
    communication request.
    """

    EMAIL_WRITING = "email_writing"
    INTERVIEW_PRACTICE = "interview_practice"
    GRAMMAR_CORRECTION = "grammar_correction"
    TONE_IMPROVEMENT = "tone_improvement"
    PUBLIC_SPEAKING = "public_speaking"
    CONFLICT_RESOLUTION = "conflict_resolution"
    CUSTOMER_COMMUNICATION = "customer_communication"