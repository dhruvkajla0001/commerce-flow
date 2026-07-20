"""
Formats analytics query results for logging.

Responsible for:
- Formatting query previews
- Logging execution statistics
- Displaying a readable DataFrame preview
"""

from __future__ import annotations

from app.analytics.exceptions import ResultFormattingError
from app.analytics.models import AnalyticsResult
from app.core.logger import get_logger

logger = get_logger(__name__)


class ResultFormatter:
    """
    Formats AnalyticsResult objects for logging.
    """

    SEPARATOR = "-" * 70

    def __init__(self, preview_rows: int = 5) -> None:
        """
        Initialize the formatter.

        Parameters
        ----------
        preview_rows : int, optional
            Number of rows to display in the preview.
            Default is 5.
        """

        self.preview_rows = preview_rows

    def display(self, result: AnalyticsResult) -> None:
        """
        Display execution summary and a preview of the query results.

        Parameters
        ----------
        result : AnalyticsResult
            Executed analytics result.
        """

        try:

            logger.info(self.SEPARATOR)
            logger.info("Analytics Result")
            logger.info(self.SEPARATOR)

            logger.info(
                "SQL File        : %s",
                result.file_name,
            )

            logger.info(
                "Execution Time  : %.3f sec",
                result.execution_time,
            )

            logger.info(
                "Rows Returned   : %d",
                result.row_count,
            )

            logger.info(
                "Columns         : %d",
                result.column_count,
            )

            if result.dataframe.empty:

                logger.warning("Query returned no rows.")
                return

            logger.info(
                "Column Names    : %s",
                ", ".join(result.dataframe.columns),
            )

            preview = result.dataframe.head(self.preview_rows)

            logger.info(
                "Preview (Top %d Rows):",
                min(self.preview_rows, result.row_count),
            )

            logger.info(
                "\n%s",
                preview.to_string(index=False),
            )

            if result.row_count > self.preview_rows:

                logger.info(
                    "... %d more rows not displayed.",
                    result.row_count - self.preview_rows,
                )

            logger.info(self.SEPARATOR)

        except Exception as exc:

            logger.exception(
                "Failed to format analytics result for '%s'.",
                getattr(result, "file_name", "Unknown"),
            )

            raise ResultFormattingError(
                str(exc)
            ) from exc