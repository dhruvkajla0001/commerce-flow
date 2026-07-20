"""
Custom exceptions for the Analytics module.
"""

from __future__ import annotations


class AnalyticsError(Exception):
    """
    Base exception for all analytics-related errors.
    """

    def __init__(self, message: str = "Analytics module error.") -> None:
        super().__init__(message)


class SQLExecutionError(AnalyticsError):
    """
    Raised when execution of a SQL query fails.
    """

    def __init__(
        self,
        sql_file: str,
        message: str,
    ) -> None:
        super().__init__(
            f"SQL execution failed for '{sql_file}': {message}"
        )


class ReportExportError(AnalyticsError):
    """
    Raised when exporting a report fails.
    """

    def __init__(
        self,
        report_file: str,
        message: str,
    ) -> None:
        super().__init__(
            f"Failed to export report '{report_file}': {message}"
        )


class ResultFormattingError(AnalyticsError):
    """
    Raised when formatting analytics results fails.
    """

    def __init__(self, message: str) -> None:
        super().__init__(
            f"Result formatting failed: {message}"
        )


class AnalyticsConfigurationError(AnalyticsError):
    """
    Raised when analytics configuration is invalid.
    """

    def __init__(self, message: str) -> None:
        super().__init__(
            f"Analytics configuration error: {message}"
        )