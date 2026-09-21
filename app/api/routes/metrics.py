"""
API monitoring metrics routes.
"""

from fastapi import APIRouter

from app.api.middleware import metrics
from app.schemas.api import MetricsResponse


router = APIRouter(
    prefix="/metrics",
    tags=["Monitoring"],
)


@router.get(
    "",
    response_model=MetricsResponse,
)
def get_metrics() -> MetricsResponse:
    """
    Return current API monitoring metrics.

    Returns:
        MetricsResponse: Current request and performance metrics.
    """
    return MetricsResponse(**metrics.get_metrics())