"""
Entry point for running the analytics pipeline.
"""

from __future__ import annotations

from app.analytics.analytics_runner import AnalyticsRunner
from app.core.logger import get_logger

logger = get_logger(__name__)


def run_analytics() -> None:
    """
    Execute the analytics pipeline.
    """

    logger.info("Starting Analytics Module...")

    runner = AnalyticsRunner()

    summary = runner.run()

    logger.info(
        "Analytics completed. Success: %d/%d",
        summary["successful"],
        summary["total_files"],
    )