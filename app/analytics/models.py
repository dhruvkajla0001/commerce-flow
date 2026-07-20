"""
Data models for the Analytics module.
"""

from __future__ import annotations

from dataclasses import dataclass
import pandas as pd


@dataclass(slots=True)
class AnalyticsResult:
    """
    Represents the execution result of a single analytics SQL file.
    """

    file_name: str

    execution_time: float

    dataframe: pd.DataFrame

    csv_path: str | None = None

    @property
    def row_count(self) -> int:
        """Return the number of rows."""
        return len(self.dataframe)

    @property
    def column_count(self) -> int:
        """Return the number of columns."""
        return len(self.dataframe.columns)