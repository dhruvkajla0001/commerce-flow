"""
Centralized logging configuration for the CommerceFlow project.

This module provides a reusable logger instance for all project modules.
Logs are written to both the console and a rotating log file.
"""

from __future__ import annotations

import logging
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
    Create and return a configured logger.

    Parameters
    ----------
    name : str
        Name of the logger (usually __name__).

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    # -------------------------------------------------------------------------
    # Console Handler
    # -------------------------------------------------------------------------

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # -------------------------------------------------------------------------
    # Rotating File Handler
    # -------------------------------------------------------------------------

    file_handler = RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=5 * 1024 * 1024,   # 5 MB
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger