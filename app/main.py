"""
FastAPI application entry point.

This module creates and configures the Communication Coach Agent API.
"""

from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.core.config import get_settings
from app.core.logging import get_logger, setup_logging
from app.api.exception_handlers import (
    communication_coach_exception_handler,
    unexpected_exception_handler,
)
from app.core.exceptions import CommunicationCoachException

setup_logging()

settings = get_settings()
logger = get_logger(__name__)

app = FastAPI(
    title=settings.app_name,
    description=(
        "Agentic AI Communication Training Agent "
        "for communication analysis and coaching."
    ),
    version="0.1.0",
    debug=settings.debug,
)
app.add_exception_handler(
    CommunicationCoachException,
    communication_coach_exception_handler,
)

app.add_exception_handler(
    Exception,
    unexpected_exception_handler,
)

app.include_router(health_router)