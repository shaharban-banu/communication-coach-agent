"""
Schemas for communication requests and agent responses.

This module defines the data contracts used between the API layer
and the agentic communication pipeline.
"""
from pydantic import BaseModel,Field
from app.agents.intent import CommunicationIntent

class CommunicationRequest(BaseModel):
    """
    Request submitted to the communication coaching system.

    Attributes:
        message: User's communication request or text to analyze.
        context: Optional contextual information about the request.
    """
    message:str=Field(...,min_length=1,description="User's communication request or text.")
    context:str |None=Field(default=None,description="Optional context relevant to the communication request.")

class CommunicationResponse(BaseModel):
    """
    Response returned by the communication coaching system.

    Attributes:
        intent: Primary communication intent detected for the request.
        response: Generated coaching or communication response.
        tools_used: Names of tools used during task execution.
        score: Optional communication score.
    """
    intent:CommunicationIntent
    response:str
    tools_used:list[str]=Field(default_factory=list)
    score:float|None=None