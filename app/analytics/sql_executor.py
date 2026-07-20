"""
SQL execution engine for the Analytics module.

Responsible for:
- Reading SQL files
- Executing SQL against PostgreSQL
- Returning results as a Pandas DataFrame
- Measuring execution time
"""

from __future__ import annotations

import time
from pathlib import Path

import pandas as pd

from app.analytics.exceptions import SQLExecutionError
from app.analytics.models import AnalyticsResult
from app.core.logger import get_logger
from app.database.connection import get_database_connection

logger = get_logger(__name__)


class SQLExecutor:
    """
    Executes analytics SQL files against PostgreSQL.
    """

    def execute(self, sql_file: Path) -> AnalyticsResult:
        """
        Execute a SQL file and return the query results.

        Parameters
        ----------
        sql_file : Path
            Path to the SQL file.

        Returns
        -------
        AnalyticsResult
            Query execution metadata and result DataFrame.
        """

        logger.info("=" * 70)
        logger.info("Executing SQL File : %s", sql_file.name)
        logger.info("=" * 70)

        sql = sql_file.read_text(encoding="utf-8")

        start_time = time.perf_counter()

        try:
            connection = get_database_connection()

            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql)

                    if cursor.description:
                        columns = [column[0] for column in cursor.description]
                        rows = cursor.fetchall()

                        dataframe = pd.DataFrame(
                            data=rows,
                            columns=columns,
                        )
                    else:
                        dataframe = pd.DataFrame()

                connection.commit()

            finally:
                connection.close()

        except Exception as exc:
            logger.exception(
                "Failed to execute SQL file: %s",
                sql_file.name,
            )

            raise SQLExecutionError(
                sql_file=sql_file.name,
                message=str(exc),
            ) from exc

        execution_time = time.perf_counter() - start_time

        logger.info(
            "Execution completed in %.3f seconds.",
            execution_time,
        )

        logger.info(
            "Rows returned: %d",
            len(dataframe),
        )

        logger.info(
            "Columns returned: %d",
            len(dataframe.columns),
        )

        return AnalyticsResult(
            file_name=sql_file.name,
            execution_time=execution_time,
            dataframe=dataframe,
        )