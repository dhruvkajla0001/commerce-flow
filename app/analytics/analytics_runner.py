"""
Analytics Runner

Responsible for:
- Discovering SQL files
- Executing analytics queries
- Formatting results
- Exporting reports
"""

from __future__ import annotations

import time
from pathlib import Path

from app.analytics.exceptions import AnalyticsError
from app.analytics.reports_exporter import ReportExporter
from app.analytics.results_formatter import ResultFormatter
from app.analytics.sql_executor import SQLExecutor
from app.core.logger import get_logger

logger = get_logger(__name__)


class AnalyticsRunner:
    """
    Orchestrates execution of analytics SQL files.
    """

    SEPARATOR = "=" * 80

    def __init__(self, sql_directory: Path | None = None) -> None:
        """
        Initialize the analytics runner.

        Parameters
        ----------
        sql_directory : Path | None
            Directory containing analytics SQL files.
            If None, the default project SQL directory is used.
        """

        project_root = Path(__file__).resolve().parents[2]

        self.sql_directory = (
            sql_directory
            if sql_directory is not None
            else project_root / "sql" / "analytics"
        )

        logger.info("Project Root : %s", project_root)
        logger.info("SQL Directory: %s", self.sql_directory)

        self.executor = SQLExecutor()
        self.formatter = ResultFormatter()
        self.exporter = ReportExporter()

    def run(self) -> dict[str, int | float]:
        """
        Execute all analytics SQL files.

        Returns
        -------
        dict
            Execution summary.
        """

        logger.info(self.SEPARATOR)
        logger.info("Starting Analytics Pipeline")
        logger.info(self.SEPARATOR)

        if not self.sql_directory.exists():
            logger.error(
                "SQL directory does not exist: %s",
                self.sql_directory,
            )

            raise FileNotFoundError(
                f"SQL directory not found: {self.sql_directory}"
            )

        sql_files = sorted(self.sql_directory.glob("*.sql"))

        if not sql_files:
            logger.warning(
                "No SQL files found in '%s'.",
                self.sql_directory,
            )

            return {
                "total_files": 0,
                "successful": 0,
                "failed": 0,
                "execution_time": 0.0,
            }

        logger.info("Discovered %d SQL files.", len(sql_files))

        pipeline_start = time.perf_counter()

        successful = 0
        failed = 0

        for sql_file in sql_files:

            logger.info(self.SEPARATOR)
            logger.info("Processing : %s", sql_file.name)
            logger.info(self.SEPARATOR)

            try:
                result = self.executor.execute(sql_file)

                self.formatter.display(result)

                self.exporter.export(result)

                successful += 1

                logger.info(
                    "Successfully processed '%s'.",
                    sql_file.name,
                )

            except AnalyticsError:

                failed += 1

                logger.exception(
                    "Analytics processing failed for '%s'.",
                    sql_file.name,
                )

            except Exception:

                failed += 1

                logger.exception(
                    "Unexpected error while processing '%s'.",
                    sql_file.name,
                )

        execution_time = time.perf_counter() - pipeline_start

        total_files = len(sql_files)

        logger.info(self.SEPARATOR)
        logger.info("Analytics Pipeline Completed")
        logger.info(self.SEPARATOR)

        logger.info("Total Files    : %d", total_files)
        logger.info("Successful     : %d", successful)
        logger.info("Failed         : %d", failed)
        logger.info("Execution Time : %.3f sec", execution_time)

        if total_files > 0:
            logger.info(
                "Success Rate   : %.2f%%",
                (successful / total_files) * 100,
            )

        logger.info(self.SEPARATOR)

        return {
            "total_files": total_files,
            "successful": successful,
            "failed": failed,
            "execution_time": execution_time,
        }


def main() -> None:
    """
    Entry point for standalone execution.
    """
    AnalyticsRunner().run()


if __name__ == "__main__":
    main()