"""
Base ETL Loader

Defines the common interface for all ETL loaders.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd

from app.core.logger import get_logger
from app.database.base import DatabaseBase

logger = get_logger(__name__)


class BaseLoader(DatabaseBase, ABC):
    """
    Abstract base class for all ETL loaders.
    """

    def __init__(self, source_file: Path) -> None:
        """
        Initialize the ETL loader.

        Parameters
        ----------
        source_file : Path
            Path to the source dataset.
        """

        super().__init__()

        self.source_file = source_file

        logger.info(
            "Initialized loader for '%s'.",
            self.source_file.name,
        )

    @abstractmethod
    def extract(self) -> pd.DataFrame:
        """
        Extract data from the source.
        """
        raise NotImplementedError

    @abstractmethod
    def transform(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Transform the extracted data.
        """
        raise NotImplementedError

    @abstractmethod
    def load(self, dataframe: pd.DataFrame) -> None:
        """
        Load the transformed data into PostgreSQL.
        """
        raise NotImplementedError

    @abstractmethod
    def run(self) -> None:
        """
        Execute the complete ETL pipeline.
        """
        raise NotImplementedError