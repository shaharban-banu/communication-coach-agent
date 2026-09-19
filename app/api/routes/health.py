"""
Health check API routes.

This module contains endpoints used to verify that the
Communication Coach Agent API is running correctly.
"""

from fastapi import APIRouter

from app.core.config import get_settings
from app.core.logging import get_logger

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)

logger = get_logger(__name__)


@router.get("")
async def health_check() -> dict[str, str]:
    """
    Check whether the API is running.

    Returns:
        dict[str, str]: Current application health status.
    """
    settings = get_settings()

    logger.info("Health check requested")

    return {
        "status": "healthy",
        "service": settings.app_name,
    }