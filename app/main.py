"""
FastAPI application entry point.

This module creates and configures the Communication Coach Agent API.
"""

from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.analyze import router as analyze_router
from app.api.routes.coach import router as coach_router
from app.api.routes.improve import router as improve_router
from app.core.config import get_settings
from app.core.logging import get_logger, setup_logging
from app.api.exception_handlers import (
    communication_coach_exception_handler,
    unexpected_exception_handler,
)
from app.core.exceptions import CommunicationCoachException
from app.api.routes.chat_history import router as chat_history_router
from app.api.middleware import RequestLoggingMiddleware
from app.api.routes.metrics import router as metrics_router

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

app.add_middleware(RequestLoggingMiddleware)
app.add_exception_handler(
    CommunicationCoachException,
    communication_coach_exception_handler,
)

app.add_exception_handler(
    Exception,
    unexpected_exception_handler,
)

app.include_router(health_router)
app.include_router(
    analyze_router,
    prefix=settings.api_v1_prefix,
)
app.include_router(
    coach_router,
    prefix=settings.api_v1_prefix,
)
app.include_router(
    improve_router,
    prefix=settings.api_v1_prefix,
)
app.include_router(
    chat_history_router,
    prefix=settings.api_v1_prefix,
)
app.include_router(
    metrics_router,
    prefix=settings.api_v1_prefix,
)