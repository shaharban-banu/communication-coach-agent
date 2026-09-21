"""
FastAPI dependency definitions.

This module provides application-level dependencies that are shared
across API requests.
"""

from functools import lru_cache

from app.agents.communication_agent import CommunicationAgent
from app.agents.factory import create_communication_agent


@lru_cache
def get_communication_agent() -> CommunicationAgent:
    """
    Return the shared CommunicationAgent instance.

    The cached instance ensures that the agent's short-term
    conversation memory is preserved across API requests.

    Returns:
        CommunicationAgent: Shared application-level agent instance.
    """
    return create_communication_agent()