"""
Data Profiler Utility

Profiles all CSV datasets inside the raw data directory and generates
summary reports for each dataset.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import json

from app.core.config import (
    RAW_DATA_DIR,
    PROFILING_REPORTS_DIR,
)
from app.core.logger import get_logger

logger = get_logger(__name__)


class DataProfiler:
    """
    Utility class responsible for profiling datasets.
    """

    def __init__(self) -> None:
        self.raw_data_dir: Path = RAW_DATA_DIR
        self.output_dir: Path = PROFILING_REPORTS_DIR

    def discover_files(self) -> list[Path]:
        """
        Discover all CSV files in the raw data directory.
        """
        csv_files = list(self.raw_data_dir.glob("*.csv"))

        logger.info("Discovered %d CSV files.", len(csv_files))

        return csv_files

    def load_dataset(self, file_path: Path) -> pd.DataFrame:
        """
        Load a CSV dataset into a pandas DataFrame.

        Parameters
        ----------
        file_path : Path
            Path to the CSV file.

        Returns
        -------
        pd.DataFrame
            Loaded dataset.
        """
        try:
            logger.info("Loading dataset: %s", file_path.name)

            dataframe = pd.read_csv(file_path)

            logger.info(
                "Successfully loaded %s (%d rows, %d columns)",
                file_path.name,
                dataframe.shape[0],
                dataframe.shape[1],
            )

            return dataframe

        except Exception as error:
            logger.exception(
                "Failed to load dataset %s",
                file_path.name,
            )
            raise error  
        

    def profile_dataset(
        self,
        file_path: Path,
        dataframe: pd.DataFrame,
    ) -> dict:
        """
        Generate a profile for a dataset.

        Parameters
        ----------
        file_path : Path
            Path of the dataset.
        dataframe : pd.DataFrame
            Loaded dataframe.

        Returns
        -------
        dict
            Dataset profiling information.
        """

        logger.info("Profiling dataset: %s", file_path.name)

        profile = {
            "dataset_name": file_path.name,
            "rows": dataframe.shape[0],
            "columns": dataframe.shape[1],
            "memory_usage_mb": round(
                dataframe.memory_usage(deep=True).sum() / (1024 * 1024),
                2,
            ),
            "duplicate_rows": int(dataframe.duplicated().sum()),
            "column_profiles": {},
        }

        for column in dataframe.columns:
            profile["column_profiles"][column] = {
                "data_type": str(dataframe[column].dtype),
                "missing_values": int(dataframe[column].isna().sum()),
                "missing_percentage": round(
                    (dataframe[column].isna().sum() / len(dataframe)) * 100,
                    2,
                ),
                "unique_values": int(dataframe[column].nunique()),
            }

        logger.info("Completed profiling: %s", file_path.name)

        return profile 


    def save_report(self, profile: dict) -> None:
        """
        Save the profiling report as a JSON file.

        Parameters
        ----------
        profile : dict
            Dataset profile.
        """

        report_file = (
            self.output_dir
            / f"{Path(profile['dataset_name']).stem}_profile.json"
        )

        with open(report_file, "w", encoding="utf-8") as file:
            json.dump(profile, file, indent=4)

        logger.info("Saved report: %s", report_file.name)   

    def run(self) -> None:
        """
        Execute the profiler.
        """

        logger.info("=" * 60)
        logger.info("Starting Data Profiler")
        logger.info("=" * 60)

        files = self.discover_files()

        for file_path in files:
            dataframe = self.load_dataset(file_path)

            profile = self.profile_dataset(
                file_path=file_path,
                dataframe=dataframe,
            )

            self.save_report(profile)

        logger.info("=" * 60)
        logger.info("Data profiling completed successfully.")
        logger.info("=" * 60)


def main() -> None:
    profiler = DataProfiler()
    profiler.run()


if __name__ == "__main__":
    main()