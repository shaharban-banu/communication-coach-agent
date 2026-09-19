"""
Centralized exception handlers for the FastAPI application.

This module converts application-specific and unexpected exceptions
into consistent HTTP responses.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AgentExecutionException,
    CommunicationCoachException,
    MemoryException,
    ToolExecutionException,
    ValidationException,
)
from app.core.logging import get_logger

logger = get_logger(__name__)


async def communication_coach_exception_handler(
    request: Request,
    exc: CommunicationCoachException,
) -> JSONResponse:
    """
    Handle application-specific exceptions.

    Args:
        request: Incoming FastAPI request.
        exc: Application-specific exception.

    Returns:
        JSONResponse: Standardized error response.
    """
    logger.warning(
        "Application error | method=%s | path=%s | error=%s",
        request.method,
        request.url.path,
        exc.message,
    )

    status_code = status.HTTP_400_BAD_REQUEST

    if isinstance(exc, ToolExecutionException):
        status_code = status.HTTP_502_BAD_GATEWAY

    elif isinstance(exc, AgentExecutionException):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    elif isinstance(exc, MemoryException):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    elif isinstance(exc, ValidationException):
        status_code = status.HTTP_400_BAD_REQUEST

    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "type": exc.__class__.__name__,
                "message": exc.message,
            }
        },
    )


async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handle unexpected application errors.

    The full exception is logged for debugging, while the client
    receives a generic message without internal implementation details.

    Args:
        request: Incoming FastAPI request.
        exc: Unexpected exception.

    Returns:
        JSONResponse: Generic internal server error response.
    """
    logger.exception(
        "Unexpected error | method=%s | path=%s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "type": "InternalServerError",
                "message": "An unexpected error occurred.",
            }
        },
    )