"""
Exports analytics query results to CSV reports.
"""

from __future__ import annotations

from pathlib import Path

from app.analytics.exceptions import ReportExportError
from app.analytics.models import AnalyticsResult
from app.core.logger import get_logger

logger = get_logger(__name__)


class ReportExporter:
    """
    Exports AnalyticsResult objects to CSV files.
    """

    def __init__(
        self,
        output_directory: Path = Path("reports") / "analytics",
    ) -> None:
        """
        Initialize the report exporter.

        Parameters
        ----------
        output_directory : Path
            Directory where CSV reports will be stored.
        """

        self.output_directory = output_directory
        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def export(self, result: AnalyticsResult) -> Path:
        """
        Export analytics results to a CSV file.

        Parameters
        ----------
        result : AnalyticsResult
            Analytics query result.

        Returns
        -------
        Path
            Path to the exported CSV file.
        """

        csv_file = (
            self.output_directory
            / f"{Path(result.file_name).stem}.csv"
        )

        try:

            result.dataframe.to_csv(
                csv_file,
                index=False,
            )

            result.csv_path = str(csv_file)

            logger.info(
                "Report exported successfully: %s",
                csv_file,
            )

            return csv_file

        except Exception as exc:

            logger.exception(
                "Failed to export report: %s",
                csv_file,
            )

            raise ReportExportError(
                report_file=str(csv_file),
                message=str(exc),
            ) from exc