"""
CSV Loader

Provides a reusable CSV extraction implementation.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.core.logger import get_logger
from app.etl.base_loader import BaseLoader

logger = get_logger(__name__)


class CSVLoader(BaseLoader):
    """
    Base loader for CSV datasets.
    """

    def __init__(self, source_file: Path) -> None:
        """
        Initialize the CSV loader.
        """

        super().__init__(source_file)

    def extract(self) -> pd.DataFrame:
        """
        Read the CSV file into a pandas DataFrame.
        """

        try:
            logger.info(
                "Reading CSV file '%s'.",
                self.source_file.name,
            )

            dataframe = pd.read_csv(self.source_file)

            logger.info(
                "Loaded %d rows and %d columns.",
                dataframe.shape[0],
                dataframe.shape[1],
            )

            return dataframe

        except Exception:
            logger.exception(
                "Failed to read '%s'.",
                self.source_file.name,
            )
            raise

    def transform(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Default transformation.
        """

        logger.info("No transformation applied.")

        return dataframe

    def load(self, dataframe: pd.DataFrame) -> None:
        """
        Placeholder for database loading.
        """

        logger.info("Load step not implemented.")

    def run(self) -> None:
        """
        Execute the ETL pipeline.
        """

        dataframe = self.extract()

        dataframe = self.transform(dataframe)

        self.load(dataframe)