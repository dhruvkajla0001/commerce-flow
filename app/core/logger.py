"""
Centralized logging configuration for the CommerceFlow project.

Supports:
- Console logging
- Rotating file logging
- Airflow log integration
"""

from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.core.config import LOG_DIR

# -----------------------------------------------------------------------------
# Logging Configuration
# -----------------------------------------------------------------------------

LOG_FILE: Path = LOG_DIR / "commerce_flow.log"

LOG_LEVEL = logging.INFO

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(filename)s:%(lineno)d | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger.

    Works for both:
    - Standalone Python execution
    - Apache Airflow tasks
    """

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Prevent duplicate handlers
    if not logger.handlers:

        formatter = logging.Formatter(
            fmt=LOG_FORMAT,
            datefmt=DATE_FORMAT,
        )

        # -------------------------------------------------------------
        # Console Handler
        # -------------------------------------------------------------
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_LEVEL)
        console_handler.setFormatter(formatter)

        # -------------------------------------------------------------
        # Rotating File Handler
        # -------------------------------------------------------------
        file_handler = RotatingFileHandler(
            filename=LOG_FILE,
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=5,
            encoding="utf-8",
        )

        file_handler.setLevel(LOG_LEVEL)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    # -------------------------------------------------------------
    # Airflow Integration
    # -------------------------------------------------------------
    #
    # Airflow configures the root logger.
    # Allow our logs to propagate so they appear
    # in the Airflow Task Logs.
    #
    if os.getenv("AIRFLOW_HOME"):
        logger.propagate = True
    else:
        logger.propagate = False

    return logger