"""
Centralized logging configuration for the application.

This module provides a consistent logging setup across all
Communication Coach Agent components.
"""

import logging
import sys

from app.core.config import get_settings


def setup_logging() -> None:
    """
    Configure application-wide logging.

    The logging level is controlled through the application settings.
    Logs are written to stdout so they can be captured by Docker,
    Render, or other deployment platforms.
    """
    settings = get_settings()

    log_level = getattr(
        logging,
        settings.log_level.upper(),
        logging.INFO,
    )

    logging.basicConfig(
        level=log_level,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Return a logger for the specified module or component.

    Args:
        name: Name of the module or component requesting the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    return logging.getLogger(name)