"""
ETL Validators

Provides reusable validation utilities for ETL pipelines.
"""

from __future__ import annotations

import pandas as pd

from app.core.logger import get_logger

logger = get_logger(__name__)


class DataValidator:
    """
    Utility class for validating datasets.
    """

    @staticmethod
    def validate_required_columns(
        dataframe: pd.DataFrame,
        required_columns: list[str],
    ) -> None:
        """
        Validate that all required columns exist.
        """

        missing_columns = [
            column
            for column in required_columns
            if column not in dataframe.columns
        ]

        if missing_columns:
            logger.error(
                "Missing required columns: %s",
                missing_columns,
            )
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        logger.info("Required column validation passed.")

    @staticmethod
    def validate_empty_dataframe(
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Validate that the dataframe is not empty.
        """

        if dataframe.empty:
            logger.error("DataFrame is empty.")
            raise ValueError("DataFrame is empty.")

        logger.info("DataFrame contains %d rows.", len(dataframe))

    @staticmethod
    def validate_duplicate_rows(
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Validate duplicate rows.
        """

        duplicates = dataframe.duplicated().sum()

        if duplicates > 0:
            logger.warning(
                "Found %d duplicate rows.",
                duplicates,
            )
        else:
            logger.info("No duplicate rows found.")

    @staticmethod
    def validate_missing_values(
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Report missing values.
        """

        missing = dataframe.isnull().sum()

        logger.info(
            "Missing values:\n%s",
            missing[missing > 0],
        )